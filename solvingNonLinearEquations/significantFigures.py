
from math import *  
def round_to_significantFigures(number, sig_figs):
  
    if number == 0:
        return 0
    
    # Calculate the power of 10 to round to
    power = sig_figs - 1 - floor(log10(abs(number)))
    
    # Round the number
    rounded = round(number * (10 ** power)) / (10 ** power)
    return rounded