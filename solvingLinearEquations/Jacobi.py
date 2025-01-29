import time
from Data import Data
from LinearSolution import LinearSolution

class Jacobi:
    def __init__(self, Data):
        self.data = Data
        self.solutions = []
        self.time = 0

    def solve_fixed_iterations(self,num_iterations,precision, initial_guess):
        """
        Solve the linear system using the Jacobi method with a fixed number of iterations,
        adding precision to each arithmetic operation.
        """
        coefficients = self.data.getA()  # Get coefficient matrix A
        for i in range(len(coefficients)):
            for j in range(len(coefficients[i])):
                coefficients[i][j] = round(coefficients[i][j] , precision)    
        results = self.data.getB()       # Get result vector B
        for i in range(len(results)):
          results[i] = round(results[i] , precision)
        n = len(coefficients)            # Number of variables
        current_solutions = [round(initial_guess, precision)] * n  # Initial guess rounded to precision

        # Initialize solutions list with empty LinearSolution objects for each iteration
        self.solutions = [LinearSolution() for _ in range(num_iterations + 1)]

        for iter_num in range(num_iterations):
            new_solutions = [0] * n  # Temporary array for the next iteration's solutions

            for i in range(n):
                # Compute the new value for the i-th variable using the old values
                sum1 = sum(
                    round(coefficients[i][j] * current_solutions[j], precision)
                    for j in range(n) if j != i
                )
                new_solutions[i] = round((results[i] - sum1) / coefficients[i][i], precision)

            # Update the current solutions
            current_solutions = new_solutions[:]

            # Store the current iteration's solutions in the corresponding LinearSolution object
            self.solutions[iter_num].setSolution(current_solutions)

        return self.solutions


    def solve_with_error(self, error_tolerance, initial_guess, precision, max_iteration):
        """Solve the linear system using the Jacobi method with error tolerance and precision."""
        coefficients = self.data.getA()  # Get coefficient matrix A
        for i in range(len(coefficients)):
            for j in range(len(coefficients[i])):
                coefficients[i][j] = round(coefficients[i][j] , precision)    
        results = self.data.getB()       # Get result vector B
        for i in range(len(results)):
          results[i] = round(results[i] , precision)
        n = len(coefficients)            # Number of variables
        current_solutions = [round(initial_guess, precision)] * n  # Initial guess rounded to precision
        previous_solutions = [float("inf")] * n  # Initialize with large values
        iteration_limit = max_iteration  # Set a default iteration limit, or based on tolerance

        # Initialize solutions list based on a maximum number of iterations
        self.solutions = [LinearSolution() for _ in range(iteration_limit + 1)]  # Assume max 100 iterations

        for iter_num in range(iteration_limit):
            new_solutions = [0] * n  # Temporary array for the next iteration's solutions

            for i in range(n):
                # Compute the new value for the i-th variable using the previous iteration's values
                sum1 = sum(
                    round(coefficients[i][j] * current_solutions[j], precision) 
                    for j in range(n) if j != i
                )
                new_solutions[i] = round((results[i] - sum1) / coefficients[i][i], precision)

            # Compute absolute relative error for each variable
            relative_errors = [
                round(abs((new_solutions[i] - current_solutions[i]) / new_solutions[i]), precision) 
                if new_solutions[i] != 0 else float("inf")
                for i in range(n)
            ]

            # Store the current iteration's solutions in the corresponding LinearSolution object
            self.solutions[iter_num].setSolution(new_solutions)

            # Check if all errors are below the tolerance
            if all(error < error_tolerance for error in relative_errors):
                # Truncate `self.solutions` to include only completed iterations
                self.solutions = self.solutions[:iter_num + 1]
                break

            # Update solutions for the next iteration
            current_solutions = new_solutions[:]

        return self.solutions

    def solve(self, iterations=None, error=None, initial=0 , precision = 15 , max_iteration= 10):
        """ Main function to solve the system of equations based on either iterations or error tolerance."""
        if iterations is not None:
          start_time = time.perf_counter()
          solution =self.solve_fixed_iterations(iterations,precision,initial_guess=initial)
          end_time = time.perf_counter()
          self.time = (end_time - start_time)*1000
          return solution
        elif error is not None:
          start_time = time.perf_counter()
          solution =self.solve_with_error(error,initial,precision,max_iteration)
          end_time = time.perf_counter()
          self.time = (end_time - start_time)*1000
          return solution
        else:
            raise ValueError("Either iterations or error tolerance must be provided.")
    def getTime(self):
      return self.time
    def toString(self):
        sol = self.solutions  
        n = len(sol)  
        ans = ""  

        for i in range(n):
            ans += f"Iteration {i}: "  
            state = sol[i].getSolutions()  
            for j in range(len(state)):
                ans += f"X{j + 1} : {state[j]} "  
            ans += "\n"  

        return ans  
