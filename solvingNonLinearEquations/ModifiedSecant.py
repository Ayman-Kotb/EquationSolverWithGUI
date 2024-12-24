from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures

def ModifiedSecant(expression, x0, delta, significantFigures, tol=0.00001, maxIterations=50):
    f = create_function_from_expression(expression)
    
    x0 = round_to_significantFigures(x0, significantFigures)
    
    it = 0
    x1 = x0
    relative_error = float('inf')
    correct_sig_figs = 0
    
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
        
        if relative_error <= tol:
            break
            
        x0 = x1
        
        if it >= maxIterations:
            print(f"Maximum iterations ({maxIterations}) reached")
            break
    
    final_fx = round_to_significantFigures(f(x1), significantFigures)
    
    return {
        'root': round_to_significantFigures(x1, significantFigures),
        'iterations': it,
        'relative_error': round_to_significantFigures(relative_error, significantFigures),
        'correct_Significant_Figures': round_to_significantFigures(correct_sig_figs, significantFigures),
        'function_value': final_fx
    }

# Example usage:
#print(ModifiedSecant("x**4-18*x**2+45", 1, 0.01, 6))