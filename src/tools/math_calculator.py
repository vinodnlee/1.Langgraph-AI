"""
Math Calculator Tool
A simple tool that performs basic mathematical operations.
"""
import math
import re
from typing import Union, Dict, Any


def math_calculator_tool(expression: str) -> Dict[str, Any]:
    """
    Evaluates mathematical expressions safely.

    Args:
        expression: Mathematical expression as string (e.g., "2 + 3 * 4")

    Returns:
        Dictionary containing calculation result and metadata
    """
    if not expression or not isinstance(expression, str):
        return {
            "error": "Invalid input: expression must be a non-empty string",
            "result": None,
            "original_expression": expression
        }

    # Clean the expression
    cleaned_expression = expression.strip()

    # Define allowed operations and functions
    allowed_names = {
        "__builtins__": {},
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
        "log": math.log,
        "log10": math.log10,
        "ceil": math.ceil,
        "floor": math.floor,
    }

    try:
        # Validate expression contains only allowed characters
        if not re.match(r'^[0-9+\-*/().\s,a-zA-Z_]+$', cleaned_expression):
            return {
                "error": "Invalid characters in expression",
                "result": None,
                "original_expression": expression
            }

        # Evaluate the expression
        result = eval(cleaned_expression, allowed_names, {})

        # Format result
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 6)  # Limit decimal places

        calculation_result = {
            "result": result,
            "original_expression": expression,
            "cleaned_expression": cleaned_expression,
            "result_type": type(result).__name__,
            "success": True
        }

        print(f"🔢 Math Calculation: {expression} = {result}")

        return calculation_result

    except ZeroDivisionError:
        return {
            "error": "Division by zero",
            "result": None,
            "original_expression": expression
        }
    except (ValueError, TypeError) as e:
        return {
            "error": f"Math error: {str(e)}",
            "result": None,
            "original_expression": expression
        }
    except Exception as e:
        return {
            "error": f"Invalid expression: {str(e)}",
            "result": None,
            "original_expression": expression
        }


# Example usage
if __name__ == "__main__":
    test_expressions = [
        "2 + 3 * 4",
        "sqrt(16) + 5",
        "sin(pi/2)",
        "10 / 2 - 1",
        "2 ** 3",  # Power operation
        "max(1, 5, 3)",
        "round(3.14159, 2)"
    ]

    print("Math Calculator Tool Examples:")
    for expr in test_expressions:
        result = math_calculator_tool(expr)
        if result.get("success"):
            print(f"  {expr} = {result['result']}")
        else:
            print(f"  {expr} -> Error: {result['error']}")
