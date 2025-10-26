"""
Advanced LangGraph workflow with conditional routing.
"""

from langgraph.graph import StateGraph, END

from src.models import GraphState


def conditional_router_node(state: GraphState) -> str:
    """
    Router node that directs flow based on input content.

    Args:
        state: Current graph state

    Returns:
        Name of the next node to execute
    """
    input_text = state.get("input_text", "")

    # Route based on input content
    if "urgent" in input_text.lower():
        return "priority_processor"
    elif "simple" in input_text.lower():
        return "simple_processor"
    else:
        return "standard_processor"


def priority_processor_node(state: GraphState) -> GraphState:
    """
    Handles urgent/priority inputs.

    Args:
        state: Current graph state

    Returns:
        Updated graph state
    """
    processed_text = f"🚨 PRIORITY: {state.get('input_text', '')}"
    print(f"🚨 Priority Processor: {processed_text}")

    return {
        **state,
        "processed_text": processed_text,
        "step": "priority_processed"
    }


def simple_processor_node(state: GraphState) -> GraphState:
    """
    Handles simple inputs with minimal processing.

    Args:
        state: Current graph state

    Returns:
        Updated graph state
    """
    processed_text = f"📝 SIMPLE: {state.get('input_text', '')}"
    print(f"📝 Simple Processor: {processed_text}")

    return {
        **state,
        "processed_text": processed_text,
        "step": "simple_processed"
    }


def standard_processor_node(state: GraphState) -> GraphState:
    """
    Handles standard inputs.

    Args:
        state: Current graph state

    Returns:
        Updated graph state
    """
    processed_text = f"⚙️ STANDARD: {state.get('input_text', '')}"
    print(f"⚙️ Standard Processor: {processed_text}")

    return {
        **state,
        "processed_text": processed_text,
        "step": "standard_processed"
    }


def create_advanced_workflow():
    """
    Creates an advanced workflow with conditional routing.

    Returns:
        Compiled LangGraph application with conditional logic
    """
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("router", conditional_router_node)
    workflow.add_node("priority_processor", priority_processor_node)
    workflow.add_node("simple_processor", simple_processor_node)
    workflow.add_node("standard_processor", standard_processor_node)

    # Set entry point
    workflow.set_entry_point("router")

    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        conditional_router_node,
        {
            "priority_processor": "priority_processor",
            "simple_processor": "simple_processor",
            "standard_processor": "standard_processor"
        }
    )

    # All processors end the workflow
    workflow.add_edge("priority_processor", END)
    workflow.add_edge("simple_processor", END)
    workflow.add_edge("standard_processor", END)

    return workflow.compile()
