
from Seidel import Seidel
from Jacobi import Jacobi
from Data import Data  # Make sure this file contains your Data class with methods getA() and getB()
from LinearSolution import LinearSolution  # The LinearSolution class should have setSolution() and getSolutions() methods

from Gauss import Gauss
from Jordan import Jordan
import time

# Assuming you have a system to solve
A = [
    [10, 2, 3, 4, 5, 6, 7, 8, 9, 1],
    [2, 11, 4, 5, 6, 7, 8, 9, 1, 3],
    [3, 4, 12, 6, 7, 8, 9, 1, 2, 5],
    [4, 5, 6, 13, 8, 9, 1, 2, 3, 6],
    [5, 6, 7, 8, 14, 1, 2, 3, 4, 7],
    [6, 7, 8, 9, 1, 15, 3, 4, 5, 8],
    [7, 8, 9, 1, 2, 3, 16, 5, 6, 9],
    [8, 9, 1, 2, 3, 4, 5, 17, 7, 10],
    [9, 1, 2, 3, 4, 5, 6, 7, 18, 11],
    [1, 3, 5, 6, 7, 8, 9, 10, 11, 19]
]
B = [55, 65, 75, 85, 95, 105, 115, 125, 135, 145]


data = Data(A, B)

jacobi = Jacobi(data)
seidel = Seidel(data)

solution1 = jacobi.solve(3)
solution2 = seidel.solve(3)


print("jacobi",jacobi.getTime())
for i, solution in enumerate(solution1):
    print(f"Iteration {i}: {solution.getSolutions()}")
    

print("seidel", seidel.getTime())
for i, solution in enumerate(solution2):
    print(f"Iteration {i}: {solution.getSolutions()}")
    
    
    
gauss = Gauss(data)
solution3 = gauss.solve()
print("gauss", solution3.getSolutions(), gauss.getTime())

    
jordon = Jordan(data)
solution4 = jordon.solve()
print("Jordan", solution4.getSolutions(),jordon.getTime())