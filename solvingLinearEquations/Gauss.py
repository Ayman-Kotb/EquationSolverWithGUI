from Data import Data
from LinearSolution import LinearSolution
import time
class Gauss:
    def __init__(self, Data):
        self.data = Data
        self.sol = LinearSolution()
        self.time =0
      

    def swap_rows(self, a, i, r, n):
        a[i], a[r] = a[r], a[i]
        return a

    def partial_pivot(self, a, i, n):
        max_val = a[i][i]
        index = -1
        for r in range(i + 1, n):
            if a[r][i] > max_val:
                max_val = a[r][i]
                index = r
        if index != -1:
            a = self.swap_rows(a, i, index, n)
        return a

    def forward_elimination(self, a, n, precision):
        for i in range(n):
            if round(a[i][i], precision) == 0.0:
                a = self.partial_pivot(a, i, n)
            for j in range(i + 1, n):
                ratio = round(a[j][i] / a[i][i], precision)
                for k in range(n + 1):    
                    a[j][k] = round(a[j][k] - ratio * a[i][k], precision)
        return a

    def back_substitution(self, a, n, precision):
        x = [0] * n
        x[n - 1] = round(a[n - 1][n] / a[n - 1][n - 1], precision)
        for i in range(n - 2, -1, -1):
            x[i] = round(a[i][n], precision)
            for j in range(i + 1, n):
                x[i] = round(x[i] - round(a[i][j] * x[j], precision), precision)
            x[i] = round(x[i] / a[i][i], precision)
        return x

    def solve(self,precision):
        start_time = time.perf_counter()
        co = self.data.getA()
        n = len(co)
        res = self.data.getB()

      
        for i in range(len(res)):
            co[i].append(res[i])
        for i in range(len(co)):
          for j in range(len(co[i])):
            co[i][j] = round(co[i][j], precision)

        a = co
        a = self.forward_elimination(a, n, precision)  
        x = self.back_substitution(a, n,precision)  
        
        
        end_time = time.perf_counter()
        self.time = (end_time - start_time)*1000
        for i in range(len(x)):
            x[i] = round(x[i],precision)
        self.sol.setSolution(x)
        return self.sol
    def getTime(self):
      return self.time
    def toString(self):
      sol = self.sol.getSolutions()  
      ans = ""
      for i in range(len(sol)):
        ans += f"X{i + 1} : {sol[i]}\n"  
      return ans
