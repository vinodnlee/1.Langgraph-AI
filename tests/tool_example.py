"""
Tool Integration Example
Demonstrates how to use tools within LangGraph workflows.
"""
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from src.models.graph_state import GraphState
from src.nodes.input_processor import input_processor_node
from src.nodes.tool_processor import tool_processor_node
from src.nodes.output_generator import output_generator_node

# Load environment variables
load_dotenv()


def create_tool_workflow():
    """
    Creates a LangGraph workflow that demonstrates tool usage.
    """
    # Create the graph
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("input_processor", input_processor_node)
    workflow.add_node("tool_processor", tool_processor_node)  # New tool node
    workflow.add_node("output_generator", output_generator_node)

    # Define the workflow edges
    workflow.set_entry_point("input_processor")
    # Route to tool processor
    workflow.add_edge("input_processor", "tool_processor")
    workflow.add_edge("tool_processor", "output_generator")
    workflow.add_edge("output_generator", END)

    # Compile the graph
    app = workflow.compile()

    return app


def run_tool_workflow(input_text: str):
    """
    Runs the tool-enhanced workflow.
    """
    print("🚀 Starting Tool-Enhanced LangGraph Workflow...")

    # Create the workflow
    app = create_tool_workflow()

    # Initial state
    initial_state = {
        "input_text": input_text,
        "processed_text": "",
        "transformed_text": "",
        "output_text": "",
        "step": "started",
        "tool_results": ""
    }

    # Run the workflow
    result = app.invoke(initial_state)

    print("=" * 60)
    print("🎉 Tool-Enhanced Workflow completed!")
    print(result["output_text"])

    # Show tool results if available
    if result.get("tool_results"):
        print("\n" + "=" * 60)
        print("🔧 Tool Results:")
        print(result["tool_results"])

    return result


# Example usage with different types of content
if __name__ == "__main__":
    examples = [
        {
            "name": "Text Analysis Example",
            "input": """
            This is a comprehensive test message for analyzing various text properties.
            It contains multiple sentences with different word lengths and structures.
            The text analyzer tool will examine word count, character count, and reading time.
            """
        },
        {
            "name": "Mathematical Content Example",
            "input": "Calculate the result: 2 + 3 * 4 and also find sqrt(16) + 10"
        },
        {
            "name": "Mixed Content Example",
            "input": "This text has 15 words and the formula pi * 2 for calculations"
        }
    ]

    for example in examples:
        print(f"\n{'='*80}")
        print(f"🔬 Running: {example['name']}")
        print(f"{'='*80}")

        result = run_tool_workflow(example['input'].strip())

        print(f"\n{'='*40}")
        print("Press Enter to continue to next example...")
        input()
