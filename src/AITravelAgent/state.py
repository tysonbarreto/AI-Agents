from typing import Annotated, List, TypedDict
from langchain_core.messages import HumanMessage, AIMessage


class PlannerState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "message in the conversation"]
    city: str
    interests: List[str]
    itinerary: str

if __name__=="__main__":
    __all__=["PlannerState"]