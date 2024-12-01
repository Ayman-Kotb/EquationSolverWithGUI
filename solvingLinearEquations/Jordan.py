from Data import Data
from Gauss import Gauss
from LinearSolution import LinearSolution
class Jordon:
  def __init__(self):
        self.data = Data()
        co = self.data.getA()
        n = len(co)
        res = self.data.getB()
        x = res
        for i in range (len(res)):
            co[i].append(res[i])
        a = co 
        self.sol = LinearSolution()
        for i in range(n):
          if a[i][i] == 0.0:
              for r in range(i+1,n):
                  if a[r][i]!= 0.0:
                      a[i], a[r] = a[r], a[i]
                      break
          max = a[i][i]
          index = -1 
          for r in range(i+1, n):
              if (a[r][i]>max) : 
                  max = a[r][i]
                  index = r
          if index!=-1:
              a[i] , a[index] = a[index] , a[i]
        for j in range(n):
          if i != j:
            ratio = a[j][i]/a[i][i]

            for k in range(n+1):
                a[j][k] = a[j][k] - ratio * a[i][k]

                          # Obtaining Solution
        for i in range(n):
          x[i] = a[i][n]/a[i][i]
        self.sol.setSolution(x)