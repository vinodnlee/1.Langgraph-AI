from langchain_core.messages import HumanMessage

from src.models.graph_state import GraphState


def input_node(state: GraphState) -> GraphState:
    """Process input and create initial message."""
    input_text = state.get("input_text", "")
    
    # Create human message
    human_message = HumanMessage(content=input_text)
    
    print(f"📥 Input: {input_text}")
    
    return {
        **state,
        "messages": [human_message]
    }
