from Data import Data
from LinearSolution import LinearSolution

class Seidel:
    def __init__(self, Data):
        self.data = Data
        self.solutions = []

    def solve_fixed_iterations(self, num_iterations):
        """Solve the linear system using the Seidel method with a fixed number of iterations."""
        coefficients = self.data.getA()  # Get coefficient matrix A
        results = self.data.getB()       # Get result vector B
        n = len(coefficients)            # Number of variables
        current_solutions = [0] * n      # Initial guess (all zeros)

        # Initialize solutions list with empty LinearSolution objects for each iteration
        self.solutions = [LinearSolution() for _ in range(num_iterations + 1)]

        for iter_num in range(num_iterations):
            # Use the current_solutions as the base for this iteration
            next_solution = current_solutions[:]

            for i in range(n):
                # Compute the sum of known values from previous steps (before updating the current variable)
                sum1 = sum(coefficients[i][j] * next_solution[j] for j in range(i))  # Using updated values for earlier variables
                sum2 = sum(coefficients[i][j] * current_solutions[j] for j in range(i + 1, n))  # Using current values for the rest
                # Calculate the new value for the i-th variable
                next_solution[i] = (results[i] - sum1 - sum2) / coefficients[i][i]

            # Store the current iteration's solutions
            self.solutions[iter_num].setSolution(next_solution)

            # Update the current solutions for the next iteration
            current_solutions = next_solution[:]

        return self.solutions

    def solve_with_error(self, error_tolerance):
        """Solve the linear system using the Seidel method with error tolerance."""
        coefficients = self.data.getA()  # Get coefficient matrix A
        results = self.data.getB()       # Get result vector B
        n = len(coefficients)            # Number of variables
        current_solutions = [0] * n      # Initial guess (all zeros)
        iteration_limit = 100  # Set a default iteration limit

        # Initialize solutions list based on a maximum number of iterations
        self.solutions = [LinearSolution() for _ in range(iteration_limit + 1)]  # Assume max 100 iterations

        for iter_num in range(iteration_limit):
            # Use the current_solutions as the base for this iteration
            next_solution = current_solutions[:]
            max_error = 0  # Initialize the maximum error

            for i in range(n):
                # Compute the sum of known values from previous steps (before updating the current variable)
                sum1 = sum(coefficients[i][j] * next_solution[j] for j in range(i))  # Using updated values for earlier variables
                sum2 = sum(coefficients[i][j] * current_solutions[j] for j in range(i + 1, n))  # Using current values for the rest
                # Calculate the new value for the i-th variable
                next_solution[i] = (results[i] - sum1 - sum2) / coefficients[i][i]

                # Compute the error for the current variable
                error_current = abs((next_solution[i] - current_solutions[i]) / next_solution[i]) if next_solution[i] != 0 else 0
                max_error = max(max_error, error_current)

            # Store the current iteration's solutions
            self.solutions[iter_num].setSolution(next_solution)

            # Check if the error tolerance has been met
            if max_error <= error_tolerance:
                # Truncate the solutions list to include only completed iterations
                self.solutions = self.solutions[:iter_num + 1]
                break

            # Update the current solutions for the next iteration
            current_solutions = next_solution[:]

        return self.solutions

    def solve(self, iterations=None, error=None):
        """ Main function to solve the system of equations based on either iterations or error tolerance."""
        if iterations is not None:
            return self.solve_fixed_iterations(iterations)
        elif error is not None:
            return self.solve_with_error(error)
        else:
            raise ValueError("Either iterations or error tolerance must be provided.")
