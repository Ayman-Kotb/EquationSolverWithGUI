from time import time
from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures

def ModifiedSecant(expression, x0, delta, significantFigures = 28, tol=0.00001, maxIterations=50):
    start_time = time()
    f = create_function_from_expression(expression)
    
    x0 = round_to_significantFigures(x0, significantFigures)
    
    it = 0
    x1 = x0
    relative_error = float('inf')
    correct_sig_figs = 0
    
    iteration_history = []

    while True:
        it += 1
        
        fx0 = round_to_significantFigures(f(x0), significantFigures)
        fx0_delta = round_to_significantFigures(f(x0 + delta), significantFigures)
        
        if abs(fx0_delta - fx0) < 1e-15:
            raise ValueError("Division by zero encountered. Method failed.")
        
        x1 = round_to_significantFigures(
            x0 - delta * fx0 / (fx0_delta - fx0), 
            significantFigures
        )
        
        if x1 != 0:
            relative_error = (abs(x1 - x0) / abs(x1)) * 100
        else:
            relative_error = abs(x1 - x0) * 100
        
        correct_sig_figs = floor(2 - log10(2 * relative_error)) if relative_error > 0 else significantFigures
        
        iteration_details = {
            'iteration': it,
            'x': round_to_significantFigures(x0, significantFigures),
            'x_plus_delta': round_to_significantFigures(x0 + delta, significantFigures),
            'x_new': round_to_significantFigures(x1, significantFigures),
            'fx': round_to_significantFigures(fx0, significantFigures),
            'fx_plus_delta': round_to_significantFigures(fx0_delta, significantFigures),
            'relative_error': round_to_significantFigures(relative_error, significantFigures),
            'sig_figs': round_to_significantFigures(correct_sig_figs, significantFigures)
        }
        iteration_history.append(iteration_details)

        if relative_error <= tol:
            break
            
        x0 = x1
        
        if it >= maxIterations:
            raise ValueError(f"Maximum iterations ({maxIterations}) reached")
    
    final_fx = round_to_significantFigures(f(x1), significantFigures)
    end_time = time()
    execution_time = end_time - start_time
    return {
        'root': round_to_significantFigures(x1, significantFigures),
        'iterations': it,
        'relative_error': round_to_significantFigures(relative_error, significantFigures) if it!=1 else "No Relative error",
        'correct_Significant_Figures': round_to_significantFigures(correct_sig_figs, significantFigures),
        'function_value': final_fx, 
        'iteration_history': iteration_history,
        'execution_time': execution_time
    }

# Example usage:
#print(ModifiedSecant("x**4-18*x**2+45", 1, 0.01, 6))