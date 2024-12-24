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
    
        matrix[i], matrix[j] = matrix[j], matrix[i]

    def find_pivot_row(self, A, k, n,precision):
        """Find the row with the largest absolute value in column k"""
        pivot_row = k
        max_value = abs(A[k][k])
        
        for i in range(k + 1, n):
            if abs(A[i][k]) > max_value:
                max_value = abs(A[i][k])
                pivot_row = i
                
        return pivot_row

    def doolittle_decomposition(self, precision):
        A = [row[:] for row in self.data.getA()]  # Create a copy of A
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]
        P = list(range(n))  # Permutation tracking

        # Initialize L's diagonal as 1
        for i in range(n):
            L[i][i] = 1.0

        for k in range(n):
            # Find pivot
            pivot_row = self.find_pivot_row(A, k, n, precision)
            if pivot_row != k:
                P[k], P[pivot_row] = P[pivot_row], P[k]
                self.swap_rows(A, k, pivot_row)
                if k > 0:
                    self.swap_rows(L, k, pivot_row)

            # Upper triangular elements
            for j in range(k, n):
                sum_uk = sum(round(L[k][p] * U[p][j], precision) for p in range(k))
                U[k][j] = round(A[k][j] - sum_uk, precision)

            # Lower triangular elements
            for i in range(k + 1, n):
                if abs(U[k][k]) < 1e-10:
                    raise ValueError("Matrix is singular or nearly singular")
                sum_lk = sum(round(L[i][p] * U[p][k], precision) for p in range(k))
                L[i][k] = round((A[i][k] - sum_lk) / U[k][k], precision)

        return L, U, P


    def crout_decomposition(self, precision):
        A = self.data.getA()
        n = len(A)
        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]

        for i in range(n):
            U[i][i] = 1.0

        for j in range(n):
            for i in range(j, n):
                sum_l = sum(round(L[i][k] * U[k][j], precision) for k in range(j))
                L[i][j] = round(A[i][j] - sum_l, precision)

            for i in range(j + 1, n):
                sum_u = sum(round(L[j][k] * U[k][i], precision) for k in range(j))
                U[j][i] = round((A[j][i] - sum_u) / L[j][j], precision)

        return L, U

    def cholesky_decomposition(self, precision):
        A = self.data.getA()
        n = len(A)
        L = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1):
                sum_k = sum(round(L[i][k] * L[j][k], precision) for k in range(j))
                if i == j:
                    if A[i][i] - sum_k <= 0:
                        raise ValueError("Matrix must be positive definite")
                    L[i][j] = round(math.sqrt(A[i][i] - sum_k), precision)
                else:
                    L[i][j] = round((A[i][j] - sum_k) / L[j][j], precision)

        return L


    def forward_substitution(self, L, b, precision):
        n = len(L)
        y = [0] * n
        for i in range(n):
            sum_ly = sum(round(L[i][j] * y[j], precision) for j in range(i))
            y[i] = round((b[i] - sum_ly) / L[i][i], precision)
        return y


    def backward_substitution(self, U, y, precision):
        n = len(U)
        x = [0] * n
        for i in range(n - 1, -1, -1):
            sum_ux = sum(round(U[i][j] * x[j], precision) for j in range(i + 1, n))
            x[i] = round((y[i] - sum_ux) / U[i][i], precision)
        return x


    def solve_doolittle(self,precision):
        a = self.data.getA()
        for i in range(len(a)):
            for j in range(len(a[i])):
              a[i][j] = round(a[i][j],precision)
        self.data.setA(a)
            
        start_time = time.perf_counter()
        b = self.data.getB()
        for i in range(len(b)):
            b[i] = round(b[i] , precision)
        self.data.setB(b)
        L, U, P = self.doolittle_decomposition(precision)
        b_permuted = [b[P[i]] for i in range(len(b))]    
        y = self.forward_substitution(L, b_permuted,precision)
    
        x = self.backward_substitution(U, y,precision)
        for i in range(len(x)):
          x[i] = round(x[i] , precision)
        self.solution.setSolution(x)
        end_time = time.perf_counter()
        self.time = (end_time - start_time)*1000
        return self.solution

    def solve_crout(self,precision):
        a = self.data.getA()
        for i in range(len(a)):
            for j in range(len(a[i])):
              a[i][j] = round(a[i][j],precision)
        self.data.setA(a)
        
        start_time = time.perf_counter()
        b = self.data.getB()
        for i in range(len(b)):
            b[i] = round(b[i] , precision)
        self.data.setB(b)
        L, U = self.crout_decomposition(precision)
        y = self.forward_substitution(L, b, precision)
        x = self.backward_substitution(U, y, precision)
        self.solution.setSolution(x)
        end_time = time.perf_counter()
        self.time = (end_time - start_time)*1000
        return self.solution
    def solve_cholesky(self,precision):
        a = self.data.getA()
        for i in range(len(a)):
            for j in range(len(a[i])):
              a[i][j] = round(a[i][j],precision)
        self.data.setA(a)
      
        start_time = time.perf_counter()
        b = self.data.getB()
        for i in range(len(b)):
            b[i] = round(b[i] , precision)
        self.data.setB(b)
        L = self.cholesky_decomposition(precision)  
        L_t = [[L[j][i] for j in range(len(L))] for i in range(len(L))]
        y = self.forward_substitution(L, b, precision)
        x = self.backward_substitution(L_t, y, precision)
        self.solution.setSolution(x)
        end_time = time.perf_counter()
        self.time = (end_time - start_time)*1000
        return self.solution
    def getTime(self):
      return self.time
    def toString(self):
      sol = self.solution.getSolutions()  
      ans = ""
      for i in range(len(sol)):
        ans += f"X{i + 1} : {sol[i]}\n"  
      return ans
