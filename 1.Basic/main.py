import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from src.models.graph_state import GraphState
from src.nodes.input_processor import input_processor_node
from src.nodes.data_transformer import data_transformer_node
from src.nodes.tool_processor import tool_processor_node
from src.nodes.output_generator import output_generator_node

# Load environment variables
load_dotenv()


def simple_router(state: GraphState) -> str:
    """
    Simple router function that decides the next node based on input length.
    """
    processed_text = state.get("processed_text", "")
    word_count = len(processed_text.split())
    
    if word_count > 10:
        print(f"🔀 Router: Long text ({word_count} words) - routing to data_transformer")
        return "data_transformer"
    else:
        print(f"🔀 Router: Short text ({word_count} words) - routing to simple_processor")
        return "simple_processor"


def simple_processor_node(state: GraphState) -> GraphState:
    """
    Simple processor for short text content.
    """
    processed_text = state.get("processed_text", "")
    
    # Simple processing for short text
    simple_text = f"📝 SIMPLE PROCESSING: {processed_text} ✨"
    
    print(f"📝 Simple Processor Node: Processed short content")
    
    return {
        **state,
        "transformed_text": simple_text,
        "step": "simple_processed"
    }


def create_langgraph_workflow():
    """
    Creates and returns the basic LangGraph workflow
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


def create_tool_enhanced_workflow():
    """
    Creates and returns the tool-enhanced LangGraph workflow
    """
    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("input_processor", input_processor_node)
    # Tool processing step
    workflow.add_node("tool_processor", tool_processor_node)
    workflow.add_node("output_generator", output_generator_node)

    # Define the workflow edges with tool processing
    workflow.set_entry_point("input_processor")
    # Route to tools first
    workflow.add_edge("input_processor", "tool_processor")
    workflow.add_edge("tool_processor", "output_generator")
    workflow.add_edge("output_generator", END)

    # Compile the graph
    app = workflow.compile()

    return app


def create_conditional_workflow():
    """
    Creates and returns a workflow with conditional routing based on text length.
    """
    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("input_processor", input_processor_node)
    workflow.add_node("data_transformer", data_transformer_node)
    workflow.add_node("simple_processor", simple_processor_node)  # New simple node
    workflow.add_node("output_generator", output_generator_node)

    # Define the workflow edges
    workflow.set_entry_point("input_processor")
    
    # Add conditional edge from input_processor
    workflow.add_conditional_edges(
        "input_processor",  # Source node
        simple_router,      # Router function
        {
            "data_transformer": "data_transformer",    # For long text
            "simple_processor": "simple_processor"     # For short text
        }
    )
    
    # Both processors lead to output generator
    workflow.add_edge("data_transformer", "output_generator")
    workflow.add_edge("simple_processor", "output_generator")
    workflow.add_edge("output_generator", END)

    # Compile the graph
    app = workflow.compile()

    return app


def run_workflow(input_text: str, use_tools: bool = False, use_conditional: bool = False):
    """
    Runs the LangGraph workflow with optional tool enhancement and conditional routing.
    
    Args:
        input_text: The input text to process
        use_tools: If True, uses the tool-enhanced workflow
        use_conditional: If True, uses conditional routing workflow
    """
    if use_conditional:
        print("🚀 Starting Conditional Routing LangGraph Workflow...")
        app = create_conditional_workflow()
    elif use_tools:
        print("🚀 Starting Tool-Enhanced LangGraph Workflow...")
        app = create_tool_enhanced_workflow()
    else:
        print("🚀 Starting Basic LangGraph Workflow...")
        app = create_langgraph_workflow()

    # Initial state
    initial_state = {
        "input_text": input_text,
        "processed_text": "",
        "transformed_text": "",
        "output_text": "",
        "step": "started"
    }
    
    # Add tool_results field if using tools
    if use_tools:
        initial_state["tool_results"] = ""

    # Run the workflow
    result = app.invoke(initial_state)

    print("=" * 60)
    if use_conditional:
        print("🎉 Conditional Routing Workflow completed!")
    elif use_tools:
        print("🎉 Tool-Enhanced Workflow completed!")
    else:
        print("🎉 Basic Workflow completed!")
    print(result["output_text"])
    
    # Show tool results if available
    if use_tools and result.get("tool_results"):
        print("\n" + "=" * 60)
        print("🔧 Tool Analysis Results:")
        print(result["tool_results"])

    return result
def run_with_tools(input_text: str):
    """
    Convenience function to run the tool-enhanced workflow.
    """
    return run_workflow(input_text, use_tools=True)


def run_with_conditional(input_text: str):
    """
    Convenience function to run the conditional routing workflow.
    """
    return run_workflow(input_text, use_conditional=True)


if __name__ == "__main__":
    # Example usage - demonstrate all three workflows
    print("🔬 LangGraph Workflow Comparison")
    print("=" * 80)
    
    # Test different inputs to show conditional routing
    test_inputs = [
        ("Short text", "Short"),  # Will route to simple_processor
        ("This is a longer message with more than ten words to test routing", "Long")  # Will route to data_transformer
    ]
    
    for input_text, description in test_inputs:
        print(f"\n� Testing with {description} Text: '{input_text}'")
        print("=" * 80)
        
        # Run basic workflow
        print("\n📋 Running Basic Workflow:")
        basic_result = run_workflow(input_text, use_tools=False)
        
        print("\n" + "-" * 80)
        
        # Run conditional workflow
        print("\n🔀 Running Conditional Routing Workflow:")
        conditional_result = run_workflow(input_text, use_conditional=True)
        
        print("\n" + "-" * 80)
        
        # Run tool-enhanced workflow
        print("\n🔧 Running Tool-Enhanced Workflow:")
        tool_result = run_workflow(input_text, use_tools=True)
        
        print("\n" + "=" * 80)
    
    print("✅ All workflow demonstrations completed!")