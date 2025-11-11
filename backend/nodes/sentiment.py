from models.schema import CustomerSupportState, QuerySentiment
from langchain_openai.chat_models import AzureChatOpenAI
import os
from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_DEPLOYMENT_NAME,
    AZURE_API_VERSION
)


llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_API_VERSION,
    openai_api_key=AZURE_OPENAI_API_KEY,
    temperature=1
)

def analyze_inquiry_sentiment(support_state: CustomerSupportState) -> CustomerSupportState:
    query = support_state['customer_query']
    prompt = f"""
    Act as a customer support agent analyzing sentiment.
    Determine sentiment from: 'Positive', 'Neutral', 'Negative'.
    Query:
    {query}
    """
    result = llm.with_structured_output(QuerySentiment).invoke(prompt)
    support_state['query_sentiment'] = result.sentiment
    return support_state
