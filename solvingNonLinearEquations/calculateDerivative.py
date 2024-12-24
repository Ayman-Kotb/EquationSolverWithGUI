from sympy import symbols, diff, parse_expr
from convertToFunc import create_function_from_expression

def create_derivative_from_expression(expression, variable='x', p=1):
    """
    Calculate symbolic derivative using SymPy.
    
    Parameters:
    expression (str): Mathematical expression as string
    variable (str): Variable to differentiate with respect to
    
    Returns:
    tuple: (derivative expression string, callable derivative function)
    """
    try:
        # Create symbolic variable and expression
        x = symbols(variable)
        expr = parse_expr(expression)
        # Calculate derivative
        derivative = diff(expr, x, p)
        derivative_str = str(derivative)
        # Convert symbolic derivative to callable function
        derivative_func = create_function_from_expression(derivative_str)
        
        return derivative_func
    except Exception as e:
        raise ValueError(f"Failed to calculate symbolic derivative: {str(e)}")
