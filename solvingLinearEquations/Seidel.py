from Data import Data
from LinearSolution import LinearSolution

class Seidel:
  def __init__(self,iterations):
        self.data = Data()
        self.solutions = [LinearSolution(iterations) for _ in range(iterations)]
