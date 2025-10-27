from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages


class GraphState(TypedDict):

    input_text: str
    processed_text: str
    transformed_text: str
    output_text: str
    step: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
