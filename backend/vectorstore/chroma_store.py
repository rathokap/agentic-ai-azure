from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
import os
from config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_DEPLOYMENT_NAME,
    AZURE_API_VERSION
)

def create_vector_db(docs):
    #os.environ["CHROMA_TELEMETRY_ENABLED"] = "True"
    print("step1")
    embed_model = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-3-small",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_version=AZURE_API_VERSION,
        openai_api_key=AZURE_OPENAI_API_KEY
    )
    print("step2")
    db = Chroma.from_documents(
        documents=docs,
        collection_name='knowledge_base',
        embedding=embed_model,
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory="./knowledge_base"
    )
    print("step3")
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.2}
    )

    return retriever
