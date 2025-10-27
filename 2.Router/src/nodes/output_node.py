"""
Output Generator Node
Generates the final output with formatting.
"""
from src.models.graph_state import GraphState


def output_node(state: GraphState) -> GraphState:
    """Generate final output."""
    messages = state.get("messages", [])
    
    # Get the last message (either direct response or tool result)
    if messages:
        last_message = messages[-1]
        output = last_message.content if hasattr(last_message, 'content') else str(last_message)
    else:
        output = "No response generated"
    
    print(f"\n📤 Output: {output}")
    
    return {
        **state,
        "output_text": output
    }