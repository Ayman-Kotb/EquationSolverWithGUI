from Data import Data
from LinearSolution import LinearSolution
import time
class Jordan:
    def __init__(self, Data):
        self.data = Data
        self.sol = LinearSolution()
        self.time = 0

    def obtain_solution(self, a, n):
        """ Obtain the solution vector x from the matrix a """
        x = [0] * n
        for i in range(n):
            x[i] = a[i][n] / a[i][i]  # Solve for each variable
        return x

    def partial_pivot(self, a, i, n):
        """ Perform partial pivoting to avoid division by zero """
        max_val = a[i][i]
        index = -1
        for r in range(i + 1, n):
            if a[r][i] > max_val:
                max_val = a[r][i]
                index = r
        if index != -1:
            a[i], a[index] = a[index], a[i]  # Swap rows
        return a

    def forward_elimination(self, a, n):
        """ Perform forward elimination for Gauss-Jordan method """
        for i in range(n):
            if a[i][i] == 0.0:
                a = self.partial_pivot(a, i, n)  # Perform partial pivot if pivot is zero

            # Normalize the pivot row
            a[i] = [x / a[i][i] for x in a[i]]

            # Eliminate all elements below the pivot
            for j in range(i + 1, n):
                ratio = a[j][i]
                for k in range(n + 1):
                    a[j][k] -= ratio * a[i][k]
        return a

    def backward_elimination(self, a, n):
        """ Perform backward elimination for Gauss-Jordan method """
        for i in range(n - 1, -1, -1):  # Start from the last row
            for j in range(i - 1, -1, -1):  # Work upwards to eliminate above pivots
                ratio = a[j][i]
                for k in range(n + 1):
                    a[j][k] -= ratio * a[i][k]
        return a

    def solve(self):
        start_time = time.perf_counter()
        co = self.data.getA()
        n = len(co)
        res = self.data.getB()

        # Append B to the matrix A
        for i in range(len(res)):
            co[i].append(res[i])

        a = co

        # Perform forward and backward elimination
        a = self.forward_elimination(a, n)
        a = self.backward_elimination(a, n)

        # Obtain the solution
        x = self.obtain_solution(a, n)
        end_time = time.perf_counter()
        self.time = (end_time - start_time)*1000
        self.sol.setSolution(x)
        return self.sol
    def getTime(self):
      return self.time  
