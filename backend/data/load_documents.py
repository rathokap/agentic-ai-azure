import json
from langchain.docstore.document import Document
from tqdm import tqdm
from typing import List

def load_documents(json_path: str) -> List[Document]:
    """
    Load and process documents from a JSON file into LangChain Document objects.
    """
    with open(json_path, "r") as f:
        knowledge_base = json.load(f)

    processed_docs = []
    for doc in tqdm(knowledge_base, desc="Processing documents"):
        metadata = doc.get('metadata', {})
        text = doc.get('text', '')
        processed_docs.append(Document(page_content=text, metadata=metadata))

    return processed_docs
