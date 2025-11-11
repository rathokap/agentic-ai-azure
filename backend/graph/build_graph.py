
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from models.schema import CustomerSupportState
from nodes.categorize import categorize_inquiry
from nodes.sentiment import analyze_inquiry_sentiment
from nodes.responses import generate_technical_response, generate_billing_response, generate_general_response
from nodes.escalate import escalate_to_human_agent
from nodes.router import determine_route
from utils.azure_checkpointer import get_checkpointer
import logging

logger = logging.getLogger(__name__)

def build_support_agent(retriever):
    # Inject retriever into response nodes if needed
    global kbase_search
    kbase_search = retriever

    graph = StateGraph(CustomerSupportState)

    graph.add_node("categorize_inquiry", categorize_inquiry)
    graph.add_node("analyze_inquiry_sentiment", analyze_inquiry_sentiment)
    graph.add_node("generate_technical_response", generate_technical_response)
    graph.add_node("generate_billing_response", generate_billing_response)
    graph.add_node("generate_general_response", generate_general_response)
    graph.add_node("escalate_to_human_agent", escalate_to_human_agent)

    graph.add_edge("categorize_inquiry", "analyze_inquiry_sentiment")
    graph.add_conditional_edges(
        "analyze_inquiry_sentiment",
        determine_route,
        [
            "generate_technical_response",
            "generate_billing_response",
            "generate_general_response",
            "escalate_to_human_agent"
        ]
    )

    graph.add_edge("generate_technical_response", END)
    graph.add_edge("generate_billing_response", END)
    graph.add_edge("generate_general_response", END)
    graph.add_edge("escalate_to_human_agent", END)

    graph.set_entry_point("categorize_inquiry")
    
    # Use Azure Table Storage checkpointer if configured, otherwise fall back to in-memory
    memory = get_checkpointer()
    logger.info(f"Using checkpointer: {type(memory).__name__}")
    
    return graph.compile(checkpointer=memory)
