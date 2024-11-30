# LinearSolution.py
import numpy as np

class LinearSolution:
    def __init__(self, num_variables):
        self.solutions = np.zeros(num_variables)  # Initialize a numpy array to hold the solutions (x1, x2, ..., xn)

    # Getter for the entire solutions array
    def getSolutions(self):
        return self.solutions

    # Setter for the solution of a specific variable (xi)
    def setSolution(self, index, value):
        if 0 <= index < len(self.solutions):
            self.solutions[index] = value
        else:
            raise IndexError("Index out of range for the solution array.")

    # Method to print the solution in a readable form
  
