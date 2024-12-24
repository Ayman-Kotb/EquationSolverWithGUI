from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures

def Secant(expression, x0, x1, significantFigures, tol=0.00001, maxIterations=50):
    f = create_function_from_expression(expression)
    
    x0 = round_to_significantFigures(x0, significantFigures)
    x1 = round_to_significantFigures(x1, significantFigures)
    
    f0 = round_to_significantFigures(f(x0), significantFigures)
    f1 = round_to_significantFigures(f(x1), significantFigures)
    
    it = 0
    x2 = x1
    relative_error = float('inf')
    correct_sig_figs = 0
    
    while True:
        it += 1
        
        if abs(f1 - f0) < 1e-15:
            raise ValueError("Division by zero encountered. Method failed.")
        
        x2 = round_to_significantFigures(x1 - f1 * (x1 - x0) / (f1 - f0), significantFigures)
        f2 = round_to_significantFigures(f(x2), significantFigures)
        
        if x2 != 0:
            relative_error = (abs(x2 - x1) / abs(x2)) * 100
        else:
            relative_error = abs(x2 - x1) * 100
        
        correct_sig_figs = floor(2 - log10(2 * relative_error)) if relative_error > 0 else significantFigures
        
        if relative_error <= tol or abs(f2) < tol:
            break
            
        x0 = x1
        x1 = x2
        f0 = f1
        f1 = f2
        
        if it >= maxIterations:
            print(f"Maximum iterations ({maxIterations}) reached")
            break
    
    return {
        'root': round_to_significantFigures(x2, significantFigures),
        'iterations': it,
        'relative_error': round_to_significantFigures(relative_error, significantFigures),
        'correct_Significant_Figures': round_to_significantFigures(correct_sig_figs, significantFigures),
        'function_value': round_to_significantFigures(f(x2), significantFigures)
    }

# Example usage:
#print(Secant("x**4-18*x**2+45", 1, 2, 6))