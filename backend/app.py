import os
import asyncio
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from graph.build_graph import build_support_agent
from utils.azure_blob_sync import get_blob_sync
import uvicorn

from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application Insights Integration (Optional)
telemetry_client = None
try:
    from config.settings import (
        APPLICATIONINSIGHTS_CONNECTION_STRING,
        USE_APPLICATION_INSIGHTS
    )
    
    if USE_APPLICATION_INSIGHTS and APPLICATIONINSIGHTS_CONNECTION_STRING:
        try:
            from opencensus.ext.azure.log_exporter import AzureLogHandler
            from applicationinsights import TelemetryClient
            
            # Add Azure Log Handler
            logger.addHandler(
                AzureLogHandler(connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING)
            )
            
            # Initialize telemetry client
            telemetry_client = TelemetryClient(APPLICATIONINSIGHTS_CONNECTION_STRING)
            logger.info("✓ Application Insights enabled")
        except ImportError as ie:
            logger.warning(f"Application Insights packages not installed: {str(ie)}")
            logger.info("Install with: pip install opencensus-ext-azure applicationinsights")
    else:
        logger.info("Application Insights disabled in configuration")
except Exception as e:
    logger.warning(f"Failed to initialize Application Insights: {str(e)}")
    telemetry_client = None


async def call_support_agent_async(agent, prompt, user_session_id, verbose=False):
    loop = asyncio.get_event_loop()
    def run_agent():
        events = agent.stream(
            {"customer_query": prompt},
            {"configurable": {"thread_id": user_session_id}},
            stream_mode="values",
        )
        last_event = None
        for event in events:
            if verbose:
                print(event)
            last_event = event
        return last_event['final_response'] if last_event else None
    result = await loop.run_in_executor(None, run_agent)
    return result

# --- FastAPI app ---
app = FastAPI(
    title="Customer Support Agent API",
    description="AI-Powered Customer Support Agent using LangGraph and Azure OpenAI",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

logger.info(f"CORS enabled for origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance - Only set if not using Azure OpenAI config
if not os.getenv("AZURE_OPENAI_API_KEY"):
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY", "AZURE_OPENAI_API_KEY")
# docs = load_documents("path/to/router_agent_documents.json")
# retriever = create_vector_db(docs)
retriever = None

# Initialize Azure Blob Storage sync for ChromaDB (Optional)
blob_sync = None
try:
    blob_sync = get_blob_sync()
    if blob_sync:
        # Try to download existing ChromaDB data from blob storage
        logger.info("Checking for existing ChromaDB backup in Azure Blob Storage...")
        if blob_sync.download_chromadb():
            logger.info("✓ ChromaDB data restored from Azure Blob Storage")
        else:
            logger.info("No existing ChromaDB backup found in Azure Blob Storage")
except Exception as e:
    logger.warning(f"Azure Blob Storage initialization failed: {str(e)}")
    blob_sync = None

# Initialize agent with error handling
try:
    agent = build_support_agent(retriever)
    logger.info("Support agent initialized successfully")
    
    # Track initialization event
    if telemetry_client:
        telemetry_client.track_event("agent_initialized", {"status": "success"})
except Exception as e:
    logger.error(f"Failed to initialize support agent: {str(e)}")
    agent = None
    
    # Track initialization failure
    if telemetry_client:
        telemetry_client.track_exception()
        telemetry_client.track_event("agent_initialized", {"status": "failed", "error": str(e)})

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Customer Support Agent API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Azure App Service"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agent_initialized": agent is not None,
        "environment": os.getenv("ENVIRONMENT", "production"),
        "azure_table_storage": os.getenv("USE_AZURE_TABLE_STORAGE", "false"),
        "azure_blob_storage": os.getenv("USE_AZURE_BLOB_STORAGE", "false"),
        "application_insights": telemetry_client is not None
    }
    
    if agent is None:
        health_status["status"] = "unhealthy"
        health_status["error"] = "Agent not initialized"
        return JSONResponse(status_code=503, content=health_status)
    
    # Track health check
    if telemetry_client:
        telemetry_client.track_metric("health_check", 1)
    
    return health_status

# Request model for better API documentation
class QueryRequest(BaseModel):
    message: str
    thread_id: str = "default"

class QueryResponse(BaseModel):
    response: str
    status: str = "success"
    thread_id: str
    sentiment: str = None
    category: str = None

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main endpoint for customer support queries (JSON body)
    
    Request body:
    - message: User's question or message
    - thread_id: Unique user session identifier (optional, defaults to 'default')
    """
    if not request.message:
        logger.warning("Empty message received")
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if agent is None:
        logger.error("Agent not initialized")
        raise HTTPException(status_code=503, detail="Service unavailable - agent not initialized")
    
    try:
        logger.info(f"Processing query for thread {request.thread_id}")
        
        # Track query event
        if telemetry_client:
            telemetry_client.track_event("query_received", {"thread_id": request.thread_id})
        
        result = await call_support_agent_async(agent, request.message, request.thread_id, verbose=False)
        logger.info(f"Query processed successfully for thread {request.thread_id}")
        
        # Track successful query
        if telemetry_client:
            telemetry_client.track_metric("query_success", 1)
            telemetry_client.track_event("query_completed", {
                "thread_id": request.thread_id,
                "status": "success"
            })
        
        return QueryResponse(
            response=result or "I apologize, but I couldn't process your request. Please try again.",
            status="success",
            thread_id=request.thread_id
        )
    except Exception as e:
        logger.error(f"Error processing query for thread {request.thread_id}: {str(e)}")
        
        # Track error
        if telemetry_client:
            telemetry_client.track_exception()
            telemetry_client.track_metric("query_error", 1)
            telemetry_client.track_event("query_failed", {
                "thread_id": request.thread_id,
                "error": str(e)
            })
        
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/support-agent")
async def support_agent_endpoint(query: str, uid: str):
    """
    Legacy endpoint for customer support queries (query parameters)
    Maintained for backwards compatibility
    
    Parameters:
    - query: User's question or message
    - uid: Unique user session identifier
    """
    request = QueryRequest(message=query, thread_id=uid)
    response = await query_endpoint(request)
    return {"result": response.response, "status": response.status}

if __name__ == "__main__":
    # Get port from environment variable (Azure sets this)
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Determine if we're in production
    is_production = os.getenv("ENVIRONMENT", "development") == "production"
    
    if is_production:
        logger.info(f"Starting in PRODUCTION mode on {host}:{port}")
    else:
        logger.info(f"Starting in DEVELOPMENT mode on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )


