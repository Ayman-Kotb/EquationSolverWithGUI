from Data import Data
from LinearSolution import LinearSolution

class Gauss:
    def __init__(self, Data):
        self.data = Data
        self.sol = LinearSolution()
      

    def swap_rows(self, a, i, r, n):
        """ Swap two rows in matrix a """
        a[i], a[r] = a[r], a[i]
        return a

    def partial_pivot(self, a, i, n):
        """ Perform partial pivoting to avoid division by zero """
        max_val = a[i][i]
        index = -1
        for r in range(i + 1, n):
            if a[r][i] > max_val:
                max_val = a[r][i]
                index = r
        if index != -1:
            a = self.swap_rows(a, i, index, n)
        return a

    def forward_elimination(self, a, n):
        """ Perform forward elimination to create upper triangular matrix """
        for i in range(n):
            if a[i][i] == 0.0:
                a = self.partial_pivot(a, i, n)
            
            for j in range(i + 1, n):
                ratio = a[j][i] / a[i][i]
                for k in range(n + 1):
                    a[j][k] -= ratio * a[i][k]
        return a

    def back_substitution(self, a, n):
        """ Perform back substitution to find the solution """
        x = [0] * n
        x[n - 1] = a[n - 1][n] / a[n - 1][n - 1]
        
        for i in range(n - 2, -1, -1):
            x[i] = a[i][n]
            for j in range(i + 1, n):
                x[i] -= a[i][j] * x[j]
            x[i] /= a[i][i]
        return x

    def solve(self):
        """ Main function to solve the system of equations using Gaussian Elimination """
        co = self.data.getA()
        n = len(co)
        res = self.data.getB()

        # Append B to the matrix A
        for i in range(len(res)):
            co[i].append(res[i])

        a = co
        a = self.forward_elimination(a, n)  # Perform forward elimination
        x = self.back_substitution(a, n)    # Perform back substitution
        
        self.sol.setSolution(x)
        return self.sol
