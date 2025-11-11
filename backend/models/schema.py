from typing import TypedDict, Literal
from pydantic import BaseModel

# State schema used in LangGraph workflow
class CustomerSupportState(TypedDict):
    customer_query: str
    query_category: str
    query_sentiment: str
    final_response: str

# Model to validate query category output from LLM
class QueryCategory(BaseModel):
    categorized_topic: Literal['Technical', 'Billing', 'General']

# Model to validate sentiment output from LLM
class QuerySentiment(BaseModel):
    sentiment: Literal['Positive', 'Negative', 'Neutral']
