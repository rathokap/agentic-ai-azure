import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# ChromaDB Configuration
CHROMA_TELEMETRY_ENABLED = os.getenv("CHROMA_TELEMETRY_ENABLED", "False")

# Azure Storage Configuration (for session management and vector store persistence)
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
AZURE_TABLE_NAME = os.getenv("AZURE_TABLE_NAME", "checkpoints")
AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME", "chromadb")

# Application Insights Configuration
APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Feature Flags
USE_AZURE_TABLE_STORAGE = os.getenv("USE_AZURE_TABLE_STORAGE", "false").lower() == "true"
USE_AZURE_BLOB_STORAGE = os.getenv("USE_AZURE_BLOB_STORAGE", "false").lower() == "true"
USE_APPLICATION_INSIGHTS = os.getenv("USE_APPLICATION_INSIGHTS", "true").lower() == "true"
