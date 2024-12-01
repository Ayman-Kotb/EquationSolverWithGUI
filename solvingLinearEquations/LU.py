from Data import Data
from LinearSolution import LinearSolution
import math
import time

class LU:
    def __init__(self, data):
        self.data = data
        self.solution = LinearSolution()
        self.time = 0 

    def swap_rows(self, matrix, i, j):
        """Swap rows i and j in the given matrix"""
        matrix[i], matrix[j] = matrix[j], matrix[i]

    def find_pivot_row(self, A, k, n):
        """Find the row with the largest absolute value in column k"""
        pivot_row = k
        max_value = abs(A[k][k])

        for i in range(k + 1, n):
            if abs(A[i][k]) > max_value:
                max_value = abs(A[i][k])
                pivot_row = i

        return pivot_row

    def doolittle_decomposition(self, precision):
        """
        Implements Doolittle's LU decomposition with partial pivoting where:
        - L has 1's on the diagonal
        - U contains the multipliers
        Returns L, U, and P (permutation matrix as list of row indices)
        """
        A = [row[:] for row in self.data.getA()]  # Create a copy of A
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        P = list(range(n))  # Permutation tracking

        # Initialize L's diagonal as 1
        for i in range(n):
            L[i][i] = 1.0

        # Perform decomposition with partial pivoting
        for k in range(n):
            # Find pivot
            pivot_row = self.find_pivot_row(A, k, n)

            if pivot_row != k:
                # Update permutation tracking
                P[k], P[pivot_row] = P[pivot_row], P[k]
                # Swap rows in A
                self.swap_rows(A, k, pivot_row)
                # Swap rows in L (only the already calculated part)
                if k > 0:
                    self.swap_rows(L, k, pivot_row)

            # Store upper triangular elements
            for j in range(k, n):
                sum_uk = sum(L[k][p] * U[p][j] for p in range(k))
                U[k][j] = A[k][j] - sum_uk
                U[k][j] = round(U[k][j], precision)  # Round the result to the given precision

            # Store lower triangular elements
            for i in range(k + 1, n):
                if abs(U[k][k]) < 1e-10:
                    raise ValueError("Matrix is singular or nearly singular")
                sum_lk = sum(L[i][p] * U[p][k] for p in range(k))
                L[i][k] = (A[i][k] - sum_lk) / U[k][k]
                L[i][k] = round(L[i][k], precision)  # Round the result to the given precision

        return L, U, P

    def crout_decomposition(self, precision):
        A = self.data.getA()
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]

        # Initialize U's diagonal as 1
        for i in range(n):
            U[i][i] = 1.0

        # Fill L and U matrices
        for j in range(n):
            # Lower triangular (L)
            for i in range(j, n):
                sum_l = sum(L[i][k] * U[k][j] for k in range(j))
                L[i][j] = A[i][j] - sum_l
                L[i][j] = round(L[i][j], precision)  # Round the result to the given precision

            # Upper triangular (U)
            for i in range(j + 1, n):
                sum_u = sum(L[j][k] * U[k][i] for k in range(j))
                U[j][i] = (A[j][i] - sum_u) / L[j][j]
                U[j][i] = round(U[j][i], precision)  # Round the result to the given precision

        return L, U

    def cholesky_decomposition(self, precision):
        A = self.data.getA()
        n = len(A)
        L = [[0.0] * n for _ in range(n)]

        # Check if matrix is symmetric
        for i in range(n):
            for j in range(n):
                if A[i][j] != A[j][i]:
                    raise ValueError("Matrix must be symmetric for Cholesky decomposition")

        # Compute L
        for i in range(n):
            for j in range(i + 1):
                sum_k = sum(L[i][k] * L[j][k] for k in range(j))

                if i == j:
                    # Diagonal elements
                    if A[i][i] - sum_k <= 0:
                        raise ValueError("Matrix must be positive definite")
                    L[i][j] = math.sqrt(A[i][i] - sum_k)
                    L[i][j] = round(L[i][j], precision)  # Round the result to the given precision
                else:
                    # Non-diagonal elements
                    L[i][j] = (A[i][j] - sum_k) / L[j][j]
                    L[i][j] = round(L[i][j], precision)  # Round the result to the given precision

        return L

    def forward_substitution(self, L, b, precision):
        """Solves Ly = b"""
        n = len(L)
        y = [0] * n
        for i in range(n):
            sum_ly = sum(L[i][j] * y[j] for j in range(i))
            y[i] = (b[i] - sum_ly) / L[i][i]
            y[i] = round(y[i], precision)  # Round each element to the precision
        return y

    def backward_substitution(self, U, y, precision):
        """Solves Ux = y"""
        n = len(U)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            sum_ux = sum(U[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - sum_ux) / U[i][i]
            x[i] = round(x[i], precision)  # Round each element to the precision
        return x

    def solve_doolittle(self, precision):
        start_time = time.perf_counter()

        """Solve using Doolittle's method with partial pivoting"""
        b = self.data.getB()
        L, U, P = self.doolittle_decomposition(precision)

        b_permuted = [b[P[i]] for i in range(len(b))]

        y = self.forward_substitution(L, b_permuted, precision)
        x = self.backward_substitution(U, y, precision)
        for i in range(len(x)):
            x[i] = round(x[i], precision)
        self.solution.setSolution(x)
        end_time = time.perf_counter()
        self.time = (end_time - start_time) * 1000
        return self.solution

    def solve_crout(self, precision):
        start_time = time.perf_counter()
        b = self.data.getB()
        L, U = self.crout_decomposition(precision)
        y = self.forward_substitution(L, b, precision)
        x = self.backward_substitution(U, y, precision)
        self.solution.setSolution(x)
        for i in range(len(x)):
            x[i] = round(x[i], precision)
        end_time = time.perf_counter()
        self.time = (end_time - start_time) * 1000
        return self.solution

    def solve_cholesky(self, precision):
        start_time = time.perf_counter()
        b = self.data.getB()
        L = self.cholesky_decomposition(precision)
        # For Cholesky, U = L^T
        L_t = [[L[j][i] for j in range(len(L))] for i in range(len(L))]
        y = self.forward_substitution(L, b, precision)
        x = self.backward_substitution(L_t, y, precision)
        for i in range(len(x)):
            x[i] = round(x[i], precision)
        self.solution.setSolution(x)
        end_time = time.perf_counter()
        self.time = (end_time - start_time) * 1000
        return self.solution

    def getTime(self):
        return self.time
