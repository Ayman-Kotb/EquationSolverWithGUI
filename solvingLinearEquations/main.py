import tkinter as tk
from tkinter import ttk, messagebox
from Gauss import Gauss
from Jordan import Jordan
from LU import LU
from Seidel import Seidel
from Jacobi import Jacobi
from Data import Data

class EquationSolverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System of Equations Solver")
        self.geometry("600x500")

        self.data = Data(a=[], b=[])
        self.variables = 2  # Default number of variables
        self.methods = ["Gauss Elimination", "Gauss-Jordan", "LU Decomposition", "Gauss-Seidel", "Jacobi-Iteration"]
        self.current_method = tk.StringVar(value=self.methods[0])
        
        self.entries = []  # Store entry widgets for coefficients and constants
        self.create_widgets()

    def create_widgets(self):
        # Variables slider
        slider_frame = tk.Frame(self)
        slider_frame.pack(pady=10)

        tk.Label(slider_frame, text="Number of Variables:").pack(side=tk.LEFT)
        self.var_slider = ttk.Scale(slider_frame, from_=2, to=15, orient=tk.HORIZONTAL, command=self.update_equations)
        self.var_slider.set(self.variables)
        self.var_slider.pack(side=tk.LEFT, padx=10)

        # Method selection
        method_frame = tk.Frame(self)
        method_frame.pack(pady=10)

        tk.Label(method_frame, text="Select Method:").pack(side=tk.LEFT)
        self.method_combo = ttk.Combobox(method_frame, values=self.methods, textvariable=self.current_method)
        self.method_combo.pack(side=tk.LEFT, padx=10)

        # LU Method selection (for LU Decomposition)
        self.lu_method_label = tk.Label(method_frame, text="LU Decomposition Method:")
        self.lu_method_label.pack(side=tk.LEFT, padx=10)
        self.lu_method_combo = ttk.Combobox(method_frame, values=["Doolittle", "Crout", "Cholesky"], textvariable=self.lu_method)
        self.lu_method_combo.pack(side=tk.LEFT, padx=10)

        # Equation input grid
        self.equation_frame = tk.Frame(self)
        self.equation_frame.pack(pady=20)
        self.create_equation_entries()

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        start_button = tk.Button(button_frame, text="Start", command=self.solve)
        start_button.pack(side=tk.LEFT, padx=10)

        quit_button = tk.Button(button_frame, text="Quit", command=self.quit)
        quit_button.pack(side=tk.LEFT, padx=10)

        # Results label
        self.results_label = tk.Label(self, text="Results will be displayed here.", font=("Arial", 12), wraplength=400)
        self.results_label.pack(pady=10)

    def create_equation_entries(self):
        # Clear existing entries
        for widget in self.equation_frame.winfo_children():
            widget.destroy()
        self.entries = []

        # Create rows for equations
        for i in range(self.variables):
            row = []
            for j in range(self.variables):
                entry = tk.Entry(self.equation_frame, width=5)
                entry.grid(row=i, column=j * 2, padx=5, pady=5)
                row.append(entry)

                if j < self.variables - 1:
                    tk.Label(self.equation_frame, text=f"x{j + 1} +").grid(row=i, column=j * 2 + 1)
                else:
                    tk.Label(self.equation_frame, text=f"x{j + 1} =").grid(row=i, column=j * 2 + 1)

            const_entry = tk.Entry(self.equation_frame, width=5)
            const_entry.grid(row=i, column=self.variables * 2 - 1, padx=5, pady=5)
            row.append(const_entry)
            self.entries.append(row)

    def update_equations(self, value):
        self.variables = int(float(value))
        self.create_equation_entries()

    def solve(self):
        # Gather input data
        try:
            self.data.a = [[float(entry.get()) for entry in row[:-1]] for row in self.entries]
            self.data.b = [float(row[-1].get()) for row in self.entries]
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")
            return

        # Solve using the selected method
        method = self.current_method.get()
        try:
            if method == "Gauss Elimination":
                solver = Gauss(self.data)
                result = solver.solve()
            elif method == "Gauss-Jordan":
                solver = Jordan(self.data)
                result = solver.solve()
            elif method == "LU Decomposition":
                solver = LU(self.data)
                if self.lu_method.get() == "Doolittle":
                    result = solver.solve_doolittle()
                elif self.lu_method.get() == "Crout":
                    result = solver.solve_crout()
                elif self.lu_method.get() == "Cholesky":
                    result = solver.solve_cholesky()
            elif method == "Gauss-Seidel":
                solver = Seidel(self.data)
                result = solver.solve()
            elif method == "Jacobi-Iteration":
                solver = Jacobi(self.data)
                result = solver.solve()
            else:
                result = "Unknown Method"
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during computation: {e}")
            return

        # Format the result vector
        result_text = "\n".join([f"x{i+1} = {ans:.4f}" for i, ans in enumerate(result)])

        # Display results
        self.results_label.config(text=f"Solution:\n{result_text}")

if __name__ == "__main__":
    app = EquationSolverApp()
    app.mainloop()
