"""
Tool Integration Node
Demonstrates how to use tools within LangGraph workflows.
"""
import json
from src.models.graph_state import GraphState
from src.tools.text_analyzer import text_analyzer_tool
from src.tools.math_calculator import math_calculator_tool


def tool_processor_node(state: GraphState) -> GraphState:
    """
    Node that demonstrates tool usage within a LangGraph workflow.

    This node analyzes the processed text and performs calculations.
    """
    processed_text = state.get("processed_text", "")

    # Use text analyzer tool
    text_analysis = text_analyzer_tool(processed_text)

    # Use math calculator tool to calculate reading efficiency
    word_count = text_analysis.get("word_count", 0)
    char_count = text_analysis.get("character_count", 0)

    # Calculate average characters per word
    if word_count > 0:
        calc_expression = f"{char_count} / {word_count}"
        calc_result = math_calculator_tool(calc_expression)
        avg_chars_per_word = calc_result.get("result", 0)
    else:
        avg_chars_per_word = 0

    # Create enhanced output with tool results
    tool_results = {
        "text_analysis": text_analysis,
        "calculations": {
            "average_chars_per_word": avg_chars_per_word,
            "reading_efficiency": "high" if avg_chars_per_word < 5 else "normal"
        }
    }

    # Enhanced text with tool insights
    enhanced_text = f"""
🔧 TOOL-ENHANCED ANALYSIS:
{processed_text}

📊 Analysis Results:
- Words: {text_analysis.get('word_count', 0)}
- Characters: {text_analysis.get('character_count', 0)}
- Sentences: {text_analysis.get('sentence_count', 0)}
- Reading Time: {text_analysis.get('reading_time_minutes', 0)} minutes
- Avg Chars/Word: {avg_chars_per_word}
- Longest Word: {text_analysis.get('longest_word', 'N/A')}

🎯 {text_analysis.get('summary', 'Analysis complete')}
    """.strip()

    print(f"🔧 Tool Processor Node: Enhanced with analysis and calculations")

    return {
        **state,
        "transformed_text": enhanced_text,
        "tool_results": json.dumps(tool_results, indent=2),
        "step": "tool_processed"
    }


# Example of a conditional tool node that chooses tools based on content
def conditional_tool_node(state: GraphState) -> GraphState:
    """
    Node that conditionally uses different tools based on content.
    """
    processed_text = state.get("processed_text", "")

    # Check if text contains numbers - use math calculator
    if any(char.isdigit() for char in processed_text):
        # Extract potential math expressions (simple heuristic)
        import re
        math_patterns = re.findall(r'[\d+\-*/().\s]+', processed_text)

        calculations = {}
        for i, pattern in enumerate(math_patterns):
            if len(pattern.strip()) > 1:  # Skip single digits
                calc_result = math_calculator_tool(pattern.strip())
                calculations[f"expression_{i}"] = calc_result

        enhanced_text = f"{processed_text}\n\n🔢 Found calculations: {calculations}"

    else:
        # Use text analyzer for non-mathematical content
        analysis = text_analyzer_tool(processed_text)
        enhanced_text = f"{processed_text}\n\n📊 Analysis: {analysis['summary']}"

    print(f"🎯 Conditional Tool Node: Applied appropriate tool")

    return {
        **state,
        "transformed_text": enhanced_text,
        "step": "conditional_tool_processed"
    }
