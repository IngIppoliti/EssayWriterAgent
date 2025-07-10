from typing import TypedDict, List
from langchain_core.pydantic_v1 import BaseModel

# A agent that want to keep track of:
  # task
  # plan 
  # draft of the essay
  # critique of theessay
  # list of documents 
  # number of revision we made
  # maximum number of 

class AgentState(TypedDict):
    task: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    revision_number: int
    max_revisions: int

class Queries(BaseModel):
    queries: List[str]
