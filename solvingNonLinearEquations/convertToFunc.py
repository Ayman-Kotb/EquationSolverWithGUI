import math
from math import *  # This gives us direct access to math functions like sin, cos, etc.

def create_function_from_expression(expression):
    """
    Convert a mathematical expression string into a callable Python function.
    Supports trigonometric functions and other math operations.
    """
    # Create a namespace with math functions
    math_namespace = {}
    # Add all math functions to namespace
    for name in dir(math):
        math_namespace[name] = getattr(math, name)
    # Add x variable placeholder
    math_namespace['x'] = None
    
    try:
        # Create the lambda function with restricted globals
        return lambda x: eval(expression, {"__builtins__": None}, 
                            {**math_namespace, 'x': x})
    except Exception as e:
        raise ValueError(f"Failed to create function from expression: {str(e)}")

