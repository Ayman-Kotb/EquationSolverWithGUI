import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from sympy import symbols, sympify, lambdify

class PlotWindow(QWidget):
    def __init__(self, equations, x_range=(-5, 5), y_range=(-5, 5), num_points=1000, title="Function Plot"):
        super().__init__()
        self.setWindowTitle("Plot Window")
        self.setGeometry(100, 100, 800, 600)

        # Set dark theme for the window
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")

        # Initial ranges
        self.x_range = x_range
        self.y_range = y_range

        # Convert the string equations to callable functions
        self.equation_funcs = [self.string_to_function(eq) for eq in equations]

        # Create the plot canvas
        self.canvas = self.create_pretty_plot(self.equation_funcs, self.x_range, self.y_range, num_points, title)

        # Create UI elements for range input
        self.x_range_input = QLineEdit(self)
        self.x_range_input.setPlaceholderText("Enter x range (min, max)")
        self.x_range_input.setText(f"{self.x_range[0]}, {self.x_range[1]}")
        self.x_range_input.setStyleSheet("background-color: #555555; color: #ffffff; border-radius: 5px; padding: 5px;")

        self.y_range_input = QLineEdit(self)
        self.y_range_input.setPlaceholderText("Enter y range (min, max)")
        self.y_range_input.setText(f"{self.y_range[0]}, {self.y_range[1]}")
        self.y_range_input.setStyleSheet("background-color: #555555; color: #ffffff; border-radius: 5px; padding: 5px;")

        self.update_button = QPushButton("Update Plot", self)
        self.update_button.clicked.connect(self.update_plot)
        self.update_button.setStyleSheet("background-color: #444444; color: #ffffff; padding: 5px 10px; border-radius: 5px;")

        # Layout for the input fields and button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.x_range_input)
        input_layout.addWidget(self.y_range_input)
        input_layout.addWidget(self.update_button)

        # Layout for the plot canvas
        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def create_pretty_plot(self, equation_funcs, x_range, y_range, num_points, title):
        """
        Creates a pretty plot of multiple mathematical functions with a dark theme.
        """
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

        x = np.linspace(x_range[0], x_range[1], num_points)
        colors = ['#2196F3', '#E91E63', '#FF9800', '#4CAF50', '#9C27B0']  # Color palette for functions

        for i, equation_func in enumerate(equation_funcs):
            try:
                y = equation_func(x)
                ax.plot(x, y, linewidth=2, color=colors[i % len(colors)], label=f'Function {i + 1}')
            except Exception as e:
                print(f"Error evaluating function {i + 1}: {e}")

        ax.set_title(title, fontsize=14, pad=20, color='white')
        ax.set_xlabel('x', fontsize=12, color='white')
        ax.set_ylabel('y', fontsize=12, color='white')
        ax.grid(True, linestyle='--', alpha=0.5, color='gray')  # Lighter grid lines
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Customize the background and axis color for dark theme
        ax.set_facecolor('#333333')
        fig.patch.set_facecolor('#2e2e2e')  # Dark background color for the entire figure

        ax.tick_params(axis='both', colors='white')  # White ticks for visibility

        # Apply y_range to limit y-axis
        ax.set_ylim(y_range)  # Set the y-axis limits based on y_range

        ax.legend(loc='upper left', fontsize=10, facecolor='#2e2e2e', edgecolor='white')  # Add legend
        plt.tight_layout()

        return FigureCanvasQTAgg(fig)

    def string_to_function(self, equation_str):
        """
        Converts a string math expression to a callable function using sympy.
        """
        x = symbols('x')  # Declare 'x' as a symbol
        sympy_expr = sympify(equation_str)  # Parse the string into a sympy expression
        equation_func = lambdify(x, sympy_expr, modules=['numpy'])  # Convert to a numpy-compatible function
        return equation_func

    def update_plot(self):
        """
        Updates the plot based on the new x and y ranges input by the user.
        """
        # Parse the x and y range values from the input fields
        try:
            x_range_str = self.x_range_input.text()
            y_range_str = self.y_range_input.text()

            # Convert the string inputs to tuples of floats
            self.x_range = tuple(map(float, x_range_str.split(',')))
            self.y_range = tuple(map(float, y_range_str.split(',')))

            # Update the plot with new ranges
            self.canvas = self.create_pretty_plot(self.equation_funcs, self.x_range, self.y_range, 1000, "Updated Plot")
            self.layout().itemAt(1).widget().setParent(None)  # Remove old canvas
            self.layout().addWidget(self.canvas)  # Add new canvas to layout

        except ValueError:
            print("Invalid range input. Please use format: min, max (e.g., -5, 5)")


# Example of using the class:
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])

    # Example list of equations
    equations = ["x**2", "x**3 - 2*x", "sin(x)"]
    window = PlotWindow(equations)
    window.show()

    app.exec_()
