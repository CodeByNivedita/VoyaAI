from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

from schemas import TravelDetails


class TravelState(TypedDict):
    # Conversation
    messages: Annotated[list[BaseMessage], add_messages]

    # Original query
    user_query: str

    # Structured information extracted from the query
    travel_details: TravelDetails | None

    # Planner
    plan: List[str]
    current_task: str

    # Tool outputs
    observations: Dict[str, Any]

    # Final response
    final_answer: str
    dashboard: Dict[str, Any]
    error: str | None