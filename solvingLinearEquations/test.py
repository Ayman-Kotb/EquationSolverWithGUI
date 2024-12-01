
from Seidel import Seidel
from Jacobi import Jacobi
from Data import Data  # Make sure this file contains your Data class with methods getA() and getB()
from LinearSolution import LinearSolution  # The LinearSolution class should have setSolution() and getSolutions() methods

from Gauss import Gauss
from Jordan import Jordan

# Assuming you have a system to solve
A = [
    [3, 1,1],
    [2, 2, 3],
    [1, 3, 2]
]
B = [9, 8, 7]

data = Data(A, B)

jacobi = Jacobi(data)
seidel = Seidel(data)

solution1 = jacobi.solve_fixed_iterations(3)
solution2 = seidel.solve_fixed_iterations(3)

print("jacobi")
for i, solution in enumerate(solution1):
    print(f"Iteration {i}: {solution.getSolutions()}")
    

print("seidel")
for i, solution in enumerate(solution2):
    print(f"Iteration {i}: {solution.getSolutions()}")
    
    
    
gauss = Gauss(data)
solution3 = gauss.solve()
print("gauss", solution3.getSolutions())

    
jordon = Jordan(data)
solution4 = jordon.solve()
print("Jordan", solution4.getSolutions())