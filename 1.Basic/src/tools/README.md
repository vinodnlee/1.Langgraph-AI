# LangGraph Tools

This folder contains reusable tools for LangGraph workflows. Tools are independent functions that can be integrated into any LangGraph node to add specific capabilities.

## Available Tools

### 1. Text Analyzer Tool (`text_analyzer.py`)

Analyzes text content and provides comprehensive metrics.

**Features:**
- Word count, character count (with/without spaces)
- Sentence and paragraph counting
- Average word length calculation
- Longest word identification
- Unique word counting
- Reading time estimation (based on 200 words/minute)
- Comprehensive summary generation

**Usage:**
```python
from src.tools.text_analyzer import text_analyzer_tool

result = text_analyzer_tool("Your text here")
print(f"Words: {result['word_count']}")
print(f"Reading time: {result['reading_time_minutes']} minutes")
```

### 2. Math Calculator Tool (`math_calculator.py`)

Safely evaluates mathematical expressions with built-in security.

**Features:**
- Basic arithmetic operations (+, -, *, /, **)
- Mathematical functions (sqrt, sin, cos, tan, log, etc.)
- Constants (pi, e)
- Utility functions (abs, round, min, max, sum)
- Safe evaluation (no arbitrary code execution)
- Error handling for invalid expressions

**Usage:**
```python
from src.tools.math_calculator import math_calculator_tool

result = math_calculator_tool("2 + 3 * 4")
if result.get("success"):
    print(f"Result: {result['result']}")
else:
    print(f"Error: {result['error']}")
```

## Integration with LangGraph

### Method 1: Direct Tool Usage in Nodes

```python
from src.models.graph_state import GraphState
from src.tools.text_analyzer import text_analyzer_tool

def my_node(state: GraphState) -> GraphState:
    text = state.get("processed_text", "")
    analysis = text_analyzer_tool(text)
    
    return {
        **state,
        "analysis_results": analysis,
        "step": "analyzed"
    }
```

### Method 2: Tool Processor Node

Use the pre-built `tool_processor_node` that demonstrates tool integration:

```python
from src.nodes.tool_processor import tool_processor_node

# Add to your workflow
workflow.add_node("tool_processor", tool_processor_node)
workflow.add_edge("input_processor", "tool_processor")
workflow.add_edge("tool_processor", "output_generator")
```

### Method 3: Conditional Tool Usage

```python
def smart_processor_node(state: GraphState) -> GraphState:
    text = state.get("processed_text", "")
    
    if any(char.isdigit() for char in text):
        # Use math calculator for numerical content
        calc_result = math_calculator_tool("extracted_expression")
        enhanced_text = f"{text}\n\nCalculation: {calc_result}"
    else:
        # Use text analyzer for text content
        analysis = text_analyzer_tool(text)
        enhanced_text = f"{text}\n\nAnalysis: {analysis['summary']}"
    
    return {
        **state,
        "transformed_text": enhanced_text,
        "step": "smart_processed"
    }
```

## Examples

### Running Tool Tests
```bash
python test_tools.py
```

### Running Tool Integration Example
```bash
python tool_example.py
```

### Sample Output

**Text Analysis:**
```
📊 Analysis Results:
- Words: 14
- Characters: 79
- Sentences: 2
- Reading Time: 0.1 minutes
- Avg Chars/Word: 5.64
- Longest Word: "sentences"
```

**Math Calculations:**
```
🔢 Math Results:
- 2 + 3 * 4 = 14
- sqrt(16) = 4.0
- pi * 2 = 6.283185
```

## Creating New Tools

To create a new tool:

1. **Create a new Python file** in the `src/tools/` directory
2. **Implement your tool function** with clear input/output types
3. **Add appropriate error handling**
4. **Update `__init__.py`** to export your tool
5. **Add tests** and examples

**Tool Template:**
```python
def my_new_tool(input_data: str) -> dict:
    """
    Description of what your tool does.
    
    Args:
        input_data: Description of input
        
    Returns:
        Dictionary with results and metadata
    """
    try:
        # Tool logic here
        result = process_input(input_data)
        
        return {
            "success": True,
            "result": result,
            "metadata": {"tool": "my_new_tool"}
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "result": None
        }
```

## Best Practices

1. **Error Handling:** Always include comprehensive error handling
2. **Type Hints:** Use proper type hints for inputs and outputs
3. **Documentation:** Include clear docstrings and examples
4. **Security:** Validate inputs and avoid unsafe operations
5. **Consistency:** Return consistent data structures
6. **Testing:** Include test cases and examples
7. **Logging:** Add appropriate print statements for debugging

## Tool Categories

- **Text Processing:** text_analyzer, text_formatter, language_detector
- **Mathematics:** math_calculator, statistics_calculator
- **Data Analysis:** data_validator, pattern_matcher
- **External APIs:** weather_api, database_connector
- **File Operations:** file_reader, csv_parser, json_validator

This modular approach allows you to build sophisticated LangGraph workflows by combining simple, reusable tools!