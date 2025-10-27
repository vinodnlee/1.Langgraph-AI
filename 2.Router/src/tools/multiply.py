"""
Multiply Tool
A simple LangChain tool that multiplies two integers.
Compatible with LangGraph's ToolNode and tools_condition.
"""
from langchain_core.tools import tool


@tool
def multiply_numbers(a: int, b: int) -> int:
    """
    Multiply two numbers together.
    
    Args:
        a: The first number to multiply
        b: The second number to multiply
        
    Returns:
        The product of a and b
    """
    result = a * b
    print(f"🔢 Multiply Numbers Tool: {a} × {b} = {result}")
    return result


# Example usage
if __name__ == "__main__":
    print("🧪 Testing Multiply Tool")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        (2, 3),
        (5, 7),
        (10, 10),
        (-4, 5),
        (0, 100)
    ]
    
    for a, b in test_cases:
        result = multiply_numbers.invoke({"a": a, "b": b})
        print(f"  {a} × {b} = {result}")
    
    print("\n✅ Multiply tool testing completed!")
