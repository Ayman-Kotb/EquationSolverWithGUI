from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures

def FixedPoint(expression, x0, significantFigures, tol=0.00001, maxIterations=50):
    g = create_function_from_expression(expression)
    
    x0 = round_to_significantFigures(x0, significantFigures)
    
    # Initialize variables
    it = 0
    x1 = x0
    relative_error = float('inf')
    correct_sig_figs = 0
    
    while True:
        it += 1
        
        x1 = round_to_significantFigures(g(x0), significantFigures)
        
        if x1 != 0:
            relative_error = (abs(x1 - x0) / abs(x1)) * 100
        else:
            relative_error = abs(x1 - x0) * 100
        
        correct_sig_figs = floor(2 - log10(2 * relative_error)) if relative_error > 0 else significantFigures
        
        if relative_error <= tol:
            break
            

        if abs(x1) > 1e10:
            raise ValueError("Method appears to be diverging. Try a different initial guess or rewrite the equation.")
            
        # Update value for next iteration
        x0 = x1
        
        # Check if maximum iterations reached
        if it >= maxIterations:
            print(f"Maximum iterations ({maxIterations}) reached")
            break
    
    # Calculate final function value (how far from being a true fixed point)
    final_error = round_to_significantFigures(abs(x1 - g(x1)), significantFigures)
    
    return {
        'root': round_to_significantFigures(x1, significantFigures),
        'iterations': it,
        'relative_error': round_to_significantFigures(relative_error, significantFigures),
        'correct_Significant_Figures': round_to_significantFigures(correct_sig_figs, significantFigures),
        'function_value': final_error
    }

# Example usage:
# For equation x^2 = 1, rewritten as x = 1/x
#print(FixedPoint("(2*x+3)**0.5", 2, 6, tol=0.001))
