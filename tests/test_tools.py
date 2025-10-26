"""
Test script for the tools we created.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.tools.text_analyzer import text_analyzer_tool
    from src.tools.math_calculator import math_calculator_tool
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run this script from the project root directory or as a module:")
    print("  python -m tests.test_tools")
    sys.exit(1)


def test_tools():
    """Test both tools with sample data."""
    print("🧪 Testing LangGraph Tools")
    print("=" * 50)

    # Test Text Analyzer
    print("\n📊 Testing Text Analyzer Tool:")
    sample_text = "This is a sample text with multiple words and sentences. It should be analyzed!"
    result = text_analyzer_tool(sample_text)

    print(f"Input: {sample_text}")
    print(f"Word count: {result['word_count']}")
    print(f"Character count: {result['character_count']}")
    print(f"Reading time: {result['reading_time_minutes']} minutes")
    print(f"Summary: {result['summary']}")

    # Test Math Calculator
    print("\n🔢 Testing Math Calculator Tool:")
    expressions = ["2 + 3 * 4", "sqrt(16)", "pi * 2", "10 / 2"]

    for expr in expressions:
        result = math_calculator_tool(expr)
        if result.get("success"):
            print(f"{expr} = {result['result']}")
        else:
            print(f"{expr} -> Error: {result['error']}")

    print("\n✅ Tool testing completed!")


if __name__ == "__main__":
    test_tools()
