from Data import Data
from LinearSolution import LinearSolution
class Gauss:
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
            index =-1 
            for r in range(i+1, n):
                if (a[r][i]>max) : 
                    max = a[r][i]
                    index = r
            if index!=-1:
                a[i] , a[index] = a[index] , a[i]
            for j in range(i+1,n):
                ratio = a[j][i]/a[i][i]
            
                for k in range(n+1):
                    a[j][k] = a[j][k] - ratio * a[i][k]

# Back Substitution
        x[n-1] = a[n-1][n]/a[n-1][n-1]

        for i in range(n-2,-1,-1):
            x[i] = a[i][n]
    
            for j in range(i+1,n):
                x[i] = x[i] - a[i][j]*x[j]
    
            x[i] = x[i]/a[i][i]
        
        self.sol.setSolution(x)



