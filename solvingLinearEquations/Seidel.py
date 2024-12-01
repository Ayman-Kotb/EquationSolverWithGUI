from Data import Data
from LinearSolution import LinearSolution
class Seidel:          
    def __init__(self, iterations=None, error=None, initial_guess=None):
        self.data = Data()
        if iterations is not None:

            self.solutions = [LinearSolution(len(self.data.b)) for _ in range(iterations)]
            
            # Initialize the first solution with the initial guess
            if initial_guess is not None:
                for i in range(len(initial_guess)):
                    self.solutions[0].setSolution(i, initial_guess[i])  # Set initial guess for the first iteration
            for k in range(1, iterations + 1):
                n = len(self.data.a)
                for j in range(n):
                    d = self.data.b[j]
                    for i in range(n):
                        if j != i:
                            if(i < j):
                                d -= self.data.a[j][i] * self.solutions[k].getSolutions()[i]
                            else:
                                d -= self.data.a[j][i] * self.solutions[k - 1].getSolutions()[i]

                    # Update the solution for the current variable
                    self.solutions[k].setSolution(j, d / self.data.a[j][j])
        elif(error is not None):
            self.solutions = [LinearSolution(len(self.data.b))]
            
            # Initialize the first solution with the initial guess
            if initial_guess is not None:
                for i in range(len(initial_guess)):
                    self.solutions[0].setSolution(i, initial_guess[i])  # Set initial guess for the first iteration

            # Continue iterating until the desired error is achieved
            k = 0
            max_error = float('inf')  # Initialize maximum error
            while max_error > error:
                k += 1
                current_solution = LinearSolution(len(self.data.b))  # New solution for current iteration
                max_error = 0  # Reset max error for this iteration
            
                n = len(self.data.a)
                for j in range(n):
                    d = self.data.b[j]
                    for i in range(n):
                        if j != i:
                            if i < j:
                                d -= self.data.a[j][i] * current_solution.getSolutions()[i]
                            else:
                                d -= self.data.a[j][i] * self.solutions[k - 1].getSolutions()[i]

                # Update the solution for the current variable
                    current_solution.setSolution(j, d / self.data.a[j][j])
                
                # Calculate the absolute relative error
                    if self.solutions[k - 1].getSolutions()[j] != 0:
                        error_current = abs((current_solution.getSolutions()[j] - self.solutions[k - 1].getSolutions()[j]) /
                                        current_solution.getSolutions()[j])
                        max_error = max(max_error, error_current)

                # Store the current solution
                self.solutions.append(current_solution)
  
