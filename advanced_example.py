from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from main import GraphState


def conditional_router_node(state: GraphState) -> str:
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
    Handles urgent/priority inputs
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
    Handles simple inputs with minimal processing
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
    Handles standard inputs
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
    Creates an advanced workflow with conditional routing
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


if __name__ == "__main__":
    # Test the advanced workflow
    app = create_advanced_workflow()

    test_cases = [
        "This is an urgent message!",
        "This is a simple request",
        "This is a normal message"
    ]

    for test_input in test_cases:
        print(f"\n🧪 Testing: {test_input}")
        result = app.invoke({"input_text": test_input, "step": "started"})
        print(f"Result: {result}")
        print("-" * 40)
