from typing import TypedDict


class GraphState(TypedDict):

    input_text: str
    processed_text: str
    transformed_text: str
    output_text: str
    step: str
