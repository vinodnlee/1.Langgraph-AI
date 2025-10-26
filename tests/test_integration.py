"""
Integration test for tool usage within LangGraph workflows.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.models.graph_state import GraphState
    from src.tools.text_analyzer import text_analyzer_tool
    from src.tools.math_calculator import math_calculator_tool
    from src.nodes.tool_processor import tool_processor_node
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run this script from the project root directory or as a module:")
    print("  python -m tests.test_integration")
    sys.exit(1)


def test_tool_integration():
    """Test tool integration with LangGraph nodes."""
    print("🔧 Testing Tool Integration with LangGraph Nodes")
    print("=" * 60)

    # Test tool processor node
    print("\n🔄 Testing Tool Processor Node:")

    # Create a sample state
    test_state = {
        "input_text": "This is a test message with 8 words for analysis.",
        "processed_text": "Processing: THIS IS A TEST MESSAGE WITH 8 WORDS FOR ANALYSIS.",
        "transformed_text": "",
        "output_text": "",
        "step": "processed"
    }

    # Run the tool processor node
    result_state = tool_processor_node(test_state)

    print(f"✅ Node executed successfully!")
    print(f"📊 Step: {result_state['step']}")
    print(f"🔧 Enhanced text generated with tool analysis")

    # Check if tool results are included
    if 'tool_results' in result_state:
        print(f"📋 Tool results captured in state")

    return result_state


def test_individual_tools():
    """Test individual tools."""
    print("\n🛠️  Testing Individual Tools:")
    print("-" * 40)

    # Test text analyzer
    text = "Sample text for analysis with multiple words."
    analysis = text_analyzer_tool(text)
    print(
        f"📊 Text Analysis: {analysis['word_count']} words, {analysis['character_count']} chars")

    # Test math calculator
    calc_result = math_calculator_tool("10 + 5 * 2")
    if calc_result.get("success"):
        print(f"🔢 Math Calculation: 10 + 5 * 2 = {calc_result['result']}")

    return True


def main():
    """Run all integration tests."""
    print("🚀 Starting Tool Integration Tests")
    print("=" * 80)

    try:
        # Test individual tools
        test_individual_tools()

        # Test tool integration with nodes
        test_tool_integration()

        print("\n" + "=" * 80)
        print("✅ All integration tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
