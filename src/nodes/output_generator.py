"""
Output Generator Node
Generates the final output with formatting
"""
from src.models.graph_state import GraphState


def output_generator_node(state: GraphState) -> GraphState:
    """
    Node 3: Output Generator
    Generates the final output with formatting
    """
    transformed_text = state.get("transformed_text", "")
    input_text = state.get("input_text", "")

    # Generate final output
    output_text = f"""
📋 LANGGRAPH WORKFLOW RESULT
═══════════════════════════
Original Input: {input_text}
Final Output: {transformed_text}
═══════════════════════════
✅ Processing completed successfully!
    """.strip()

    print("📤 Output Generator Node: Final output generated")

    return {
        **state,
        "output_text": output_text,
        "step": "output_generated"
    }
