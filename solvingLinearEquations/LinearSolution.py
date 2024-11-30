class LinearSolution:
    def __init__(self, num_variables):
        self.solutions = [0] * num_variables  

    def get_solutions(self):
        return self.solutions

    def set_solutions(self, values):
        if len(values) == len(self.solutions):
            self.solutions = values
        else:
            raise ValueError(f"Expected {len(self.solutions)} solutions, got {len(values)}.")

  
