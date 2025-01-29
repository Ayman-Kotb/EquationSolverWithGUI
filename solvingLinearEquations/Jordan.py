from Data import Data
from LinearSolution import LinearSolution
import time
class Jordan:
    def __init__(self, Data):
        self.data = Data
        self.sol = LinearSolution()
        self.time = 0

    def obtain_solution(self, a, n, precision):
      x = [0] * n
      for i in range(n):
        x[i] = round(a[i][n] / a[i][i], precision)
      return x

    def partial_pivot(self, a, i, n):
        max_val = a[i][i]
        index = -1
        for r in range(i + 1, n):
            if abs(a[r][i]) > abs(max_val):  
                max_val = a[r][i]
                index = r
        if index != -1:
            a[i], a[index] = a[index], a[i]
        return a

    def forward_elimination(self, a, n, precision):
        for i in range(n):
            if round(a[i][i], precision) == 0.0:
                a = self.partial_pivot(a, i, n)
            
            a[i] = [round(x / a[i][i], precision) for x in a[i]]
            
            for j in range(i + 1, n):
                ratio = round(a[j][i], precision)
                for k in range(n + 1):
                    a[j][k] = round(a[j][k] - ratio * a[i][k], precision)
        return a

    def backward_elimination(self, a, n, precision):
        for i in range(n - 1, -1, -1):  
            for j in range(i - 1, -1, -1):  
                ratio = round(a[j][i], precision)
                for k in range(n + 1):
                    a[j][k] = round(a[j][k] - ratio * a[i][k], precision)
        return a

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

        a = self.forward_elimination(a, n,precision)
        a = self.backward_elimination(a, n,precision)

        x = self.obtain_solution(a, n, precision)
        end_time = time.perf_counter()
        self.time = (end_time - start_time)*1000
        for i in range(len(x)):
            x[i] = round(x[i] , precision)
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