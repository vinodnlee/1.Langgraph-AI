"""
Input Processor Node
Processes the initial input and adds some context
"""
from src.models.graph_state import GraphState


def input_processor_node(state: GraphState) -> GraphState:
    """
    Node 1: Input Processor
    Processes the initial input and adds some context
    """
    input_text = state.get("input_text", "")

    # Simple processing - add a prefix and clean the input
    processed_text = f"Processing: {input_text.strip().upper()}"

    print(f"🔍 Input Processor Node: {processed_text}")

    return {
        **state,
        "processed_text": processed_text,
        "step": "input_processed"
    }
