from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures
from calculateDerivative import create_derivative_from_expression

def Modified1_Newton_Raphson(expression, xi, significantFigures=28, m=1, tol=0.00001, maxIterations=50):
    f = create_function_from_expression(expression)
    df = create_derivative_from_expression(expression)
   
    xi = round_to_significantFigures(xi, significantFigures)

    f_xi = round_to_significantFigures(f(xi), significantFigures)
    df_xi = round_to_significantFigures(df(xi), significantFigures)

    it = 0
    iterations = []
    relative_error = float('inf')
    correct_sig_figs = 0

    # Store initial values
    iterations.append({
        'iteration': it,
        'x': xi,
        'f(x)': f_xi,
        'f\'(x)': df_xi,
        'relative_error': None
    })

    while it < maxIterations:
        it += 1
        if df_xi == 0:
            raise ValueError("Division by zero, method failed")
        
        previous_xi = xi
        # Modified Newton step with multiplicity m
        xi = round_to_significantFigures(previous_xi - m * (f_xi / df_xi), significantFigures)
        
        f_xi = round_to_significantFigures(f(xi), significantFigures)
        df_xi = round_to_significantFigures(df(xi), significantFigures)
        
        # Calculate relative error
        if abs(xi) > 1e-15:  # Avoid division by very small numbers
            relative_error = abs(xi - previous_xi) / abs(xi) * 100
        else:
            relative_error = abs(xi - previous_xi) * 100
            
        correct_sig_figs = max(0, floor(2 - log10(2 * relative_error))) if relative_error > 0 else significantFigures
        
        # Store current iteration data
        iterations.append({
            'iteration': it,
            'x': xi,
            'f(x)': f_xi,
            'f\'(x)': df_xi,
            'relative_error': round_to_significantFigures(relative_error, significantFigures)
        })
        
        # Check convergence conditions
        if abs(f_xi) < tol or relative_error < tol:
            break
            
    if it >= maxIterations:
        raise ValueError(f"Warning: Maximum iterations ({maxIterations}) reached")
    
    return {
        'root': round_to_significantFigures(xi, significantFigures),
        'iterations': it,
        'relative_error': round_to_significantFigures(relative_error, significantFigures),
        'correct_Significant_Figures': correct_sig_figs,
        'function_value': round_to_significantFigures(f_xi, significantFigures),
        'iteration_history': iterations
    }

print(Modified1_Newton_Raphson("x**2",2, m=2)) 
