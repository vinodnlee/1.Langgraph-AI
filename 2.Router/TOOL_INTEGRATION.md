# Tool Integration in LangGraph

This document explains the different approaches to integrating tools in LangGraph workflows.

## Overview

We have implemented three different workflow approaches:

1. **Basic Sequential Workflow** - No tools, just sequential node processing
2. **Custom Tool Node Workflow** - Manual tool integration with custom node
3. **ToolNode Workflow** - Using LangGraph's prebuilt `ToolNode` and `tools_condition`

## Approach 1: Basic Sequential Workflow

The simplest approach with no tool integration.

```python
def create_basic_workflow():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("input_processor", input_processor_node)
    workflow.add_node("data_transformer", data_transformer_node)
    workflow.add_node("output_generator", output_generator_node)
    
    workflow.set_entry_point("input_processor")
    workflow.add_edge("input_processor", "data_transformer")
    workflow.add_edge("data_transformer", "output_generator")
    workflow.add_edge("output_generator", END)
    
    return workflow.compile()
```

**Use Case**: Simple workflows without tool requirements.

## Approach 2: Custom Tool Node

Manual tool integration where you create a custom node that calls tools directly.

```python
# Custom node that directly calls the multiply tool
def multiply_node(state: GraphState) -> GraphState:
    processed_text = state.get("processed_text", "")
    
    # Extract numbers from text
    numbers = [int(word) for word in processed_text.split() if word.isdigit()]
    
    if len(numbers) >= 2:
        # Directly call the multiply function
        result = multiply(numbers[0], numbers[1])
        
        return {
            **state,
            "output_text": f"Result: {result}",
            "step": "multiply_completed"
        }
    
    return state
```

**Workflow Setup**:
```python
def create_workflow_with_multiply():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("input_processor", input_processor_node)
    workflow.add_node("data_transformer", data_transformer_node)
    workflow.add_node("multiply_node", multiply_node)  # Custom tool node
    workflow.add_node("output_generator", output_generator_node)
    
    workflow.set_entry_point("input_processor")
    workflow.add_edge("input_processor", "data_transformer")
    workflow.add_edge("data_transformer", "multiply_node")
    workflow.add_edge("multiply_node", "output_generator")
    workflow.add_edge("output_generator", END)
    
    return workflow.compile()
```

**Pros**:
- Full control over tool execution
- Simple to understand
- Direct function calls

**Cons**:
- Manual implementation required
- No automatic tool routing
- More boilerplate code

## Approach 3: ToolNode with tools_condition (Recommended)

Using LangGraph's prebuilt components for automatic tool handling.

### Step 1: Define Tools with @tool Decorator

```python
from langchain_core.tools import tool

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together."""
    result = a * b
    print(f"🔢 Multiply Numbers Tool: {a} × {b} = {result}")
    return result

# Create tools list
tools = [multiply_numbers]
```

### Step 2: Update GraphState with Messages

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    input_text: str
    processed_text: str
    transformed_text: str
    output_text: str
    step: str
    messages: Annotated[Sequence[BaseMessage], add_messages]  # Required for ToolNode
```

### Step 3: Create Agent Node

```python
from langchain_core.messages import AIMessage

def agent_node(state: GraphState) -> GraphState:
    """Agent that decides whether to call tools."""
    processed_text = state.get("processed_text", "")
    
    # Logic to determine if tools are needed
    if any(word.isdigit() for word in processed_text.split()):
        numbers = [int(word) for word in processed_text.split()
                   if word.replace('-', '').isdigit()]
        
        if len(numbers) >= 2:
            # Create AIMessage with tool_calls
            ai_message = AIMessage(
                content="",
                tool_calls=[{
                    "name": "multiply_numbers",
                    "args": {"a": numbers[0], "b": numbers[1]},
                    "id": "call_1"
                }]
            )
            
            return {
                **state,
                "messages": [ai_message],
                "step": "agent_requesting_tool"
            }
    
    # No tools needed
    return {
        **state,
        "step": "agent_completed"
    }
```

### Step 4: Create Workflow with ToolNode

```python
from langgraph.prebuilt import ToolNode, tools_condition

def create_workflow_with_tool_node():
    workflow = StateGraph(GraphState)
    
    # Add standard nodes
    workflow.add_node("input_processor", input_processor_node)
    workflow.add_node("data_transformer", data_transformer_node)
    workflow.add_node("agent", agent_node)
    
    # Create and add ToolNode
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)
    
    workflow.add_node("output_generator", output_generator_node)
    
    # Define edges
    workflow.set_entry_point("input_processor")
    workflow.add_edge("input_processor", "data_transformer")
    workflow.add_edge("data_transformer", "agent")
    
    # Conditional edge using tools_condition
    workflow.add_conditional_edges(
        "agent",
        tools_condition,  # Automatically checks for tool_calls
        {
            "tools": "tools",      # If tools needed, go to tool node
            END: "output_generator"  # Otherwise, go to output
        }
    )
    
    workflow.add_edge("tools", "output_generator")
    workflow.add_edge("output_generator", END)
    
    return workflow.compile()
```

## Key Differences

| Feature | Custom Node | ToolNode + tools_condition |
|---------|-------------|---------------------------|
| Setup Complexity | Simple | Moderate |
| Tool Routing | Manual | Automatic |
| State Requirements | Any state structure | Requires `messages` field |
| Tool Format | Direct function calls | @tool decorator + AIMessage |
| Flexibility | High | High |
| Boilerplate | More | Less |
| LangChain Integration | Optional | Built-in |

## When to Use Each Approach

### Use Basic Workflow When:
- No tool requirements
- Simple sequential processing
- Quick prototypes

### Use Custom Tool Node When:
- Simple tool integration
- Full control over execution
- Custom tool handling logic
- Don't need LangChain ecosystem

### Use ToolNode + tools_condition When:
- Multiple tools
- Complex tool routing
- LangChain/LangSmith integration
- Agentic workflows
- Production applications
- Want automatic tool orchestration

## Best Practices

1. **Always use @tool decorator** for ToolNode integration
2. **Include `messages` field** in GraphState when using ToolNode
3. **Create AIMessage with tool_calls** for proper tool routing
4. **Use tools_condition** for automatic conditional routing
5. **Keep agent logic separate** from tool execution
6. **Handle both tool and non-tool paths** in your workflow

## Testing

All three approaches are tested in `main.py`:

```python
# Test 1: Basic workflow
result1 = run_workflow("Hello LangGraph!", use_multiply=False)

# Test 2: Custom multiply node
result2 = run_workflow("Calculate 12 and 8", use_multiply=True)

# Test 3: ToolNode approach
result3 = run_workflow("Process numbers 15 and 7", use_tool_node=True)
```

## Example Output

### ToolNode Workflow:
```
🚀 Starting Workflow with ToolNode...
🔍 Input Processor Node: PROCESSED: PROCESS NUMBERS 15 AND 7...
🔄 Data Transformer Node: Added enhancements
🤖 Agent Node: Requesting tool call - multiply 15 × 7
🔢 Multiply Numbers Tool: 15 × 7 = 105
📤 Output Generator Node: Final output generated
```

The workflow automatically:
1. Processes input
2. Agent detects numbers and creates tool call
3. tools_condition routes to ToolNode
4. ToolNode executes multiply_numbers tool
5. Results merge back into state
6. Continues to output generation

## Conclusion

For modern LangGraph applications, **ToolNode + tools_condition** is the recommended approach as it:
- Reduces boilerplate code
- Provides automatic tool routing
- Integrates seamlessly with LangChain ecosystem
- Scales well for multiple tools
- Enables agentic patterns

The custom node approach remains valid for simple use cases or when you need complete control over tool execution.
