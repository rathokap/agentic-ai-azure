
from langchain_openai.chat_models import AzureChatOpenAI
import os
from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_DEPLOYMENT_NAME,
    AZURE_API_VERSION
)

# Initialize the AzureChatOpenAI model
llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_API_VERSION,
    openai_api_key=AZURE_OPENAI_API_KEY,
    temperature=1
)
