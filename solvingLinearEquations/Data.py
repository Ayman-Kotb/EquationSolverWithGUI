class Data:
    def __init__(self, a, b):
      
        self.a = a
        self.b = b

    # Getter for matrix A
    def getA(self):
        return self.a

    # Setter for matrix A
    def setA(self, a):
        self.a = a

    # Getter for vector b
    def getB(self):
        return self.b

    # Setter for vector b
    def setB(self, b):
        self.b = b

    # Method to display the data in a readable form
    def __str__(self):
        return f"Matrix A:\n{self.a}\nVector b:\n{self.b}"
