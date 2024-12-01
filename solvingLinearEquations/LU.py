from Data import Data
from LinearSolution import LinearSolution
import math

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

    def doolittle_decomposition(self):
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

            # Store lower triangular elements
            for i in range(k + 1, n):
                if abs(U[k][k]) < 1e-10:
                    raise ValueError("Matrix is singular or nearly singular")
                sum_lk = sum(L[i][p] * U[p][k] for p in range(k))
                L[i][k] = (A[i][k] - sum_lk) / U[k][k]

        return L, U, P

    def crout_decomposition(self):
    
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

            # Upper triangular (U)
            for i in range(j + 1, n):
                sum_u = sum(L[j][k] * U[k][i] for k in range(j))
                U[j][i] = (A[j][i] - sum_u) / L[j][j]

        return L, U

    def cholesky_decomposition(self):
        
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
                else:
                    # Non-diagonal elements
                    L[i][j] = (A[i][j] - sum_k) / L[j][j]

        return L

    def forward_substitution(self, L, b):
        """Solves Ly = b"""
        n = len(L)
        y = [0] * n
        for i in range(n):
            sum_ly = sum(L[i][j] * y[j] for j in range(i))
            y[i] = (b[i] - sum_ly) / L[i][i]
        return y

    def backward_substitution(self, U, y):
        """Solves Ux = y"""
        n = len(U)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            sum_ux = sum(U[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (y[i] - sum_ux) / U[i][i]
        return x

    def solve_doolittle(self):
        """Solve using Doolittle's method with partial pivoting"""
        b = self.data.getB()
        L, U, P = self.doolittle_decomposition()
        
        
        b_permuted = [b[P[i]] for i in range(len(b))]
        
        
        y = self.forward_substitution(L, b_permuted)
        
        
        x = self.backward_substitution(U, y)
        
        self.solution.setSolution(x)
        return self.solution

    def solve_crout(self):
       
        b = self.data.getB()
        L, U = self.crout_decomposition()
        y = self.forward_substitution(L, b)
        x = self.backward_substitution(U, y)
        self.solution.setSolution(x)
        return self.solution

    def solve_cholesky(self):
     
        b = self.data.getB()
        L = self.cholesky_decomposition()
        # For Cholesky, U = L^T
        L_t = [[L[j][i] for j in range(len(L))] for i in range(len(L))]
        y = self.forward_substitution(L, b)
        x = self.backward_substitution(L_t, y)
        self.solution.setSolution(x)
        return self.solution