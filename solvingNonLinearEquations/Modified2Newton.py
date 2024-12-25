from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures
from calculateDerivative import create_derivative_from_expression

def Modified2_Newton_Raphson(expression, xi, significantFigures, tol=0.00001, maxIterations=50):

    f = create_function_from_expression(expression)
    df = create_derivative_from_expression(expression)
    d2f = create_derivative_from_expression(expression, p=2)
   
    xi = round_to_significantFigures(xi, significantFigures)
    
    f_xi = round_to_significantFigures(f(xi), significantFigures)
    df_xi = round_to_significantFigures(df(xi), significantFigures)
    d2f_xi = round_to_significantFigures(d2f(xi), significantFigures)

    it = 0

    iterations = []

    if f_xi != 0:    
        previous_xi = xi
        correct_sig_figs = 0

        # Store initial values
        iterations.append({
            'iteration': it,
            'x': xi,
            'f(x)': f_xi,
            'f\'(x)': df_xi,
            'f\'\'(x)': d2f_xi,
            'relative_error': None
        })
    
        while True:
            it += 1
            
            numerator = round_to_significantFigures(f_xi * df_xi, significantFigures)
            denominator = round_to_significantFigures(df_xi**2 - d2f_xi * f_xi, significantFigures)

            if denominator == 0:
                raise ValueError("division by zero, method failed")
            
            xi = round_to_significantFigures(previous_xi - numerator / denominator, significantFigures)
        
            f_xi = round_to_significantFigures(f(xi), significantFigures)
        
            if xi != 0:
                relative_error = abs(xi - previous_xi) / abs(xi) * 100
            else:
                relative_error = abs(xi - previous_xi) * 100
        
            correct_sig_figs = floor(2 - log10(2 * relative_error)) if relative_error > 0 else significantFigures
        
            if relative_error <= tol:
                break
                
            if f_xi == 0:  
                break
        
            previous_xi = xi

            df_xi = round_to_significantFigures(df(xi), significantFigures)
            d2f_xi = round_to_significantFigures(d2f(xi), significantFigures)

            # Store current iteration data
            iterations.append({
                'iteration': it,
                'x': xi,
                'f(x)': f_xi,
                'f\'(x)': df_xi,
                'f\'\'(x)': d2f_xi,
                'relative_error': round_to_significantFigures(relative_error, significantFigures)
            })
        
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

print(Modified2_Newton_Raphson("3*x**4+6.1*x**3-2*x**2+3*x+2 ",0 ,6 ,tol=0.01)) 
