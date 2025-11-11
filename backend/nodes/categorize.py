from models.schema import CustomerSupportState, QueryCategory
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

def categorize_inquiry(support_state: CustomerSupportState) -> CustomerSupportState:
    query = support_state['customer_query']
    prompt = f"""
                Act as a customer support agent trying to best categorize the customer query.
                          You are an agent for an AI products and hardware company.

                          Please read the customer query below and
                          determine the best category from the following list:
                          'Technical', 'Billing', 'General'.

                          Remember:
                           - Technical queries will focus more on technical aspects like AI models, hardware, software related queries etc.
                           - General queries will focus more on general aspects like contacting support, finding things, policies etc.
                           - Billing queries will focus more on payment and purchase related aspects

                          Return just the category name (from one of the above)

                          Query:{query}
    """
    result = llm.with_structured_output(QueryCategory).invoke(prompt)
    support_state['query_category'] = result.categorized_topic
    return support_state
