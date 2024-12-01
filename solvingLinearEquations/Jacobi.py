from Data import Data
from LinearSolution import LinearSolution

class Jacobi:
    def __init__(self, Data):
        self.data = Data
        self.solutions = []

    def solve_fixed_iterations(self, num_iterations):
        """Solve the linear system using the Jacobi method with a fixed number of iterations."""
        coefficients = self.data.getA()  # Get coefficient matrix A
        results = self.data.getB()       # Get result vector B
        n = len(coefficients)            # Number of variables
        current_solutions = [0] * n      # Initial guess (all zeros)

        # Initialize solutions list with empty LinearSolution objects for each iteration
        self.solutions = [LinearSolution() for _ in range(num_iterations+1)]

        for iter_num in range(num_iterations):
            new_solutions = [0] * n  # Temporary array for the next iteration's solutions

            for i in range(n):
                # Compute the new value for the i-th variable using the old values
                sum1 = sum(coefficients[i][j] * current_solutions[j] for j in range(n) if j != i)
                new_solutions[i] = (results[i] - sum1) / coefficients[i][i]

            # Update the current solutions
            current_solutions = new_solutions[:]

            # Store the current iteration's solutions in the corresponding LinearSolution object
            self.solutions[iter_num].setSolution(current_solutions)

        return self.solutions

    def solve_with_error(self, error_tolerance):
        """Solve the linear system using the Jacobi method with error tolerance."""
        coefficients = self.data.getA()  # Get coefficient matrix A
        results = self.data.getB()       # Get result vector B
        n = len(coefficients)            # Number of variables
        current_solutions = [0] * n      # Initial guess (all zeros)
        previous_solutions = [float("inf")] * n  # Initialize with large values
        iteration_limit = 100  # Set a default iteration limit, or based on tolerance

        # Initialize solutions list based on a maximum number of iterations
        self.solutions = [LinearSolution() for _ in range(iteration_limit+1)]  # Assume max 100 iterations

        for iter_num in range(iteration_limit):
            new_solutions = [0] * n  # Temporary array for the next iteration's solutions

            for i in range(n):
                # Compute the new value for the i-th variable using the previous iteration's values
                sum1 = sum(coefficients[i][j] * current_solutions[j] for j in range(n) if j != i)
                new_solutions[i] = (results[i] - sum1) / coefficients[i][i]

            # Compute absolute relative error for each variable
            relative_errors = [
                abs((new_solutions[i] - current_solutions[i]) / new_solutions[i]) if new_solutions[i] != 0 else float("inf")
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

    def solve(self, iterations=None, error=None):
        """ Main function to solve the system of equations based on either iterations or error tolerance."""
        if iterations is not None:
            return self.solve_fixed_iterations(iterations)
        elif error is not None:
            return self.solve_with_error(error)
        else:
            raise ValueError("Either iterations or error tolerance must be provided.")
