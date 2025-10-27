"""
Basic LangGraph workflow with 3 sequential nodes.
"""

from langgraph.graph import StateGraph, END

from src.models import GraphState
from src.nodes import (
    input_processor_node,
    data_transformer_node,
    output_generator_node
)


def create_langgraph_workflow():
    """
    Creates and returns the basic LangGraph workflow.

    Returns:
        Compiled LangGraph application
    """
    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("input_processor", input_processor_node)
    workflow.add_node("data_transformer", data_transformer_node)
    workflow.add_node("output_generator", output_generator_node)

    # Define the workflow edges
    workflow.set_entry_point("input_processor")
    workflow.add_edge("input_processor", "data_transformer")
    workflow.add_edge("data_transformer", "output_generator")
    workflow.add_edge("output_generator", END)

    # Compile the graph
    app = workflow.compile()

    return app


def run_workflow(input_text: str):
    """
    Run the LangGraph workflow with given input.

    Args:
        input_text: Input text to process

    Returns:
        Final workflow state with results
    """
    print("🚀 Starting LangGraph Workflow...")
    print("=" * 50)

    # Create the workflow
    app = create_langgraph_workflow()

    # Initial state
    initial_state = {
        "input_text": input_text,
        "processed_text": "",
        "transformed_text": "",
        "output_text": "",
        "step": "started"
    }

    # Run the workflow
    result = app.invoke(initial_state)

    print("=" * 50)
    print("🎉 Workflow completed!")
    print(result["output_text"])

    return result
