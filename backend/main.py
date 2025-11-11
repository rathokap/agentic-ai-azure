
import os
import json
from langchain.docstore.document import Document
from tqdm import tqdm
from vectorstore.chroma_store import create_vector_db
from graph.build_graph import build_support_agent
import asyncio
from IPython.display import Markdown
from IPython.display import display, Image, Markdown

# Load documents from JSON file
#def load_documents(json_path):
    #with open(json_path, "r") as f:
        #knowledge_base = json.load(f)
    #processed_docs = []
    #for doc in tqdm(knowledge_base):
        #metadata = doc['metadata']
        #data = doc['text']
        #processed_docs.append(Document(page_content=data, metadata=metadata))
    #return processed_docs

# Run the agent with a query

# Synchronous version for CLI usage
def call_support_agent(agent, prompt, user_session_id, verbose=False):
    events = agent.stream(
        {"customer_query": prompt},
        {"configurable": {"thread_id": user_session_id}},
        stream_mode="values",
    )
    print(events)
    print('Running Agent. Please wait...')
    for event in events:
        if verbose:
            print(event)
    display(Markdown(event['final_response']))
    return event['final_response']


# Global agent instance for CLI usage
os.environ['OPENAI_API_KEY'] = "AZURE_OPENAI_API_KEY"
#docs = load_documents("C:\\Users\\patimsur\\OneDrive - Tietoevry\\AI\\Agents\\LangGraph\\New customer\\data\\router_agent_documents.json")
#retriever = create_vector_db(docs)
retriever = None
agent = build_support_agent(retriever)

if __name__ == "__main__":
    # For CLI usage
    print("ok")
    uid = "suraj"
    query = "do you support on-prem models?"
    call_support_agent(agent, query, uid, verbose=True)
    # To run the API: uvicorn main:app --reload
