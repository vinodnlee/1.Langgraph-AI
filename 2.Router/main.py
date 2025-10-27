import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.models.graph_state import GraphState
from src.nodes.input_node import input_node
from src.nodes.output_node import output_node
from src.tools.multiply import multiply_numbers

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define tools and bind to LLM
tools = [multiply_numbers]
llm_with_tools = llm.bind_tools(tools)



def agent_node(state: GraphState) -> GraphState:
    """
    LLM agent that decides whether to call multiply tool or respond directly.
    """
    messages = state.get("messages", [])
    
    # Call LLM with tools
    response = llm_with_tools.invoke(messages)
    
    print(f"🤖 Agent: Analyzing request...")
    
    # Check if LLM wants to call tools
    if response.tool_calls:
        print(f"   → Tool call requested: {response.tool_calls[0]['name']}")
    else:
        print(f"   → Direct response: {response.content}")
    
    return {
        **state,
        "messages": [response]
    }


def should_continue(state: GraphState) -> str:
    """Determine if we should call tools or end."""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None
    
    # Use tools_condition logic
    if last_message and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return "end"





def create_workflow():
    """Create the simplified LangGraph workflow."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("input_processor", input_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("output", output_node)
    
    # Define edges
    workflow.set_entry_point("input_processor")
    workflow.add_edge("input_processor", "agent")
    
    # Conditional routing: agent → tools or end
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": "output"
        }
    )
    
    # After tools, go back to agent for final response
    workflow.add_edge("tools", "agent")
    workflow.add_edge("output", END)
    
    return workflow.compile()


def run_workflow(input_text: str):
    """Run the workflow."""
    print("=" * 60)
    print("🚀 Starting LangGraph Workflow with LLM Agent")
    print("=" * 60)
    
    app = create_workflow()
    
    # Initial state
    initial_state = {
        "input_text": input_text,
        "processed_text": "",
        "transformed_text": "",
        "output_text": "",
        "step": "",
        "messages": []
    }
    
    # Run workflow
    result = app.invoke(initial_state)
    
    print("=" * 60)
    print("✅ Workflow completed!")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║    LangGraph + LLM Agent with Tool Routing Demo         ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # Test 1: Multiplication request
    print("\n📋 Test 1: Multiplication Request")
    print("-" * 60)
    result1 = run_workflow("What is 15 multiplied by 8?")
    
    # Test 2: Non-multiplication question
    print("\n\n📋 Test 2: General Question")
    print("-" * 60)
    result2 = run_workflow("What is the capital of France?")
    
    # Test 3: Another multiplication
    print("\n\n📋 Test 3: Another Multiplication")
    print("-" * 60)
    result3 = run_workflow("Calculate 25 times 4")
    
    print("\n\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)



