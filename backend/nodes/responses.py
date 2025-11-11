from models.schema import CustomerSupportState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
import os
from vectorstore.chroma_store import create_vector_db
from langchain.docstore.document import Document
from tqdm import tqdm
import json
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
def load_documents(json_path):
    with open(json_path, "r") as f:
        knowledge_base = json.load(f)
    processed_docs = []
    for doc in tqdm(knowledge_base):
        metadata = doc['metadata']
        data = doc['text']
        processed_docs.append(Document(page_content=data, metadata=metadata))
    return processed_docs
docs = load_documents("./data/router_agent_documents.json")
retriever = create_vector_db(docs)

def generate_response(support_state: CustomerSupportState, category: str) -> CustomerSupportState:
    query = support_state['customer_query']
    metadata_filter = {'category': category.lower()}
    retriever.search_kwargs['filter'] = metadata_filter
    relevant_docs = retriever.invoke(query)
    retrieved_content = "".join(doc.page_content for doc in relevant_docs)

    prompt = ChatPromptTemplate.from_template(f"""
    Craft a detailed {category} support response.
    Use the knowledge base below. If unknown, say:
    'Apologies I was not able to answer your question, please reach out to +1-xxxx-xxxx'
    Customer Query:
    {{customer_query}}
    Relevant Knowledge Base Information:
    {{relevant_content}}
    """)

    chain = prompt | llm
    reply = chain.invoke({"customer_query": query, "relevant_content": retrieved_content}).content
    support_state['final_response'] = reply
    return support_state

def generate_technical_response(support_state: CustomerSupportState) -> CustomerSupportState:
    return generate_response(support_state, "Technical")

def generate_billing_response(support_state: CustomerSupportState) -> CustomerSupportState:
    return generate_response(support_state, "Billing")

def generate_general_response(support_state: CustomerSupportState) -> CustomerSupportState:
    return generate_response(support_state, "General")
