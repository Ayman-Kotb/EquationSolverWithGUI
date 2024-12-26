from math import *
from convertToFunc import create_function_from_expression
from significantFigures import round_to_significantFigures

def Bisection(expression, a, b, significantFigures = 28, tol=0.00001, maxIterations=50):
   
    f = create_function_from_expression(expression)
    
    
    a = round_to_significantFigures(a, significantFigures)
    b = round_to_significantFigures(b, significantFigures)
    
    if a >= b:
        raise ValueError("(b) must be greater than (a)")
    
   
    fa = round_to_significantFigures(f(a), significantFigures)
    fb = round_to_significantFigures(f(b), significantFigures)
    
    if fa * fb >= 0:
        raise ValueError("method may fail.")
    
    iterations = []
    it = 0
    previous_c = round_to_significantFigures(a, significantFigures)
    c = previous_c 
    
    while True:
        it += 1
        
        c = round_to_significantFigures((a + b) / 2, significantFigures)
        fc = round_to_significantFigures(f(c), significantFigures)
        
        
        if c != 0:
            relative_error = (abs(c - previous_c) / abs(c))*100
        else:
            relative_error =(abs(c - previous_c))*100

        iteration_data = {
            'iteration': it,
            'xl': round_to_significantFigures(a, significantFigures),
            'xu': round_to_significantFigures(b, significantFigures),
            'xr': round_to_significantFigures(c, significantFigures),
            'f(xr)': round_to_significantFigures(fc, significantFigures),
            'relative_error': round_to_significantFigures(relative_error, significantFigures)
        }
        iterations.append(iteration_data)
        
        if relative_error <= tol:
            break
        
        if relative_error > 0:
                correct_sig_figs = floor(2 - log10(2 * relative_error))
        else:
                correct_sig_figs = significantFigures
        if fc == 0:
            break
        elif fa * fc< 0:
            b = c
        else:
            a = c
            fa = fc
        
        previous_c = c
        
        
        if it >= maxIterations:
            print(f"Maximum iterations ({maxIterations}) reached")
            break
    
    return {
        'root': round_to_significantFigures(c, significantFigures),
        'iterations': it,
        'relative_error': round_to_significantFigures(relative_error, significantFigures),
        'correct_Significant_Figures': round_to_significantFigures(correct_sig_figs, significantFigures),
        'function_value': round_to_significantFigures(f(c), significantFigures),
        'iteration_history': iterations 
    }
    
    
    
# print(Bisection("sin(x)- x**2 ", 0.5, 1, 6,tol=2)) 
# print(Bisection("3*x**4+6.1*x**3-2*x**2+3*x+2 ", -1, 0,6,tol=0.01)) 
#result = Bisection("sin(x)- x**2 ", 0.5, 1, 6, tol=2)
#for iteration in result['iteration_history']:
    #print(f"Iteration {iteration['iteration']}:")
    #print(f"  xl = {iteration['xl']}")
    #print(f"  xu = {iteration['xu']}")
    #print(f"  xr = {iteration['xr']}")
    #print(f"  f(xr) = {iteration['f(xr)']}")
    #print(f"  relative error = {iteration['relative_error']}%")
