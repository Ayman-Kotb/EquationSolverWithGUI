import sys
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                           QPushButton, QLineEdit, QLabel, QMessageBox, QApplication)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

class PlotWindow(QMainWindow):
    def __init__(self, equation=""):
        super().__init__()
        self.equation = equation
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Equation Plotter")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #0d0d0d;")

        # Create central widget and main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create input area
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)

        # Equation input
        self.equation_input = QLineEdit()
        self.equation_input.setText(self.equation)
        self.equation_input.setPlaceholderText("Enter equation (use 'x' as variable, e.g., x^2 + 2*x + 1)")
        self.equation_input.setStyleSheet("""
            QLineEdit {
                background-color: #181a18;
                color: white;
                border: 2px solid #181a18;
                border-radius: 10px;
                padding: 5px;
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        # Range inputs
        self.x_min_input = QLineEdit()
        self.x_min_input.setPlaceholderText("X min")
        self.x_max_input = QLineEdit()
        self.x_max_input.setPlaceholderText("X max")
        for input_field in [self.x_min_input, self.x_max_input]:
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: #181a18;
                    color: white;
                    border: 2px solid #181a18;
                    border-radius: 10px;
                    padding: 5px;
                    height: 15px;
                    width: 60px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

        # Range labels
        x_range_label = QLabel("X Range:")
        x_range_label.setStyleSheet("color: white; font-size: 14px;")
        equation_label = QLabel("Equation:")
        equation_label.setStyleSheet("color: white; font-size: 14px;")

        # Update button
        update_button = QPushButton("Update Plot")
        update_button.clicked.connect(self.update_plot)
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #181a18;
                color: #249c06;
                border: 2px solid #181a18;
                border-radius: 10px;
                padding: 5px;
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #249c06;
                color: #ccc;
                border: 2px solid #249c06;
            }
        """)

        # Add widgets to input layout
        input_layout.addWidget(equation_label)
        input_layout.addWidget(self.equation_input)
        input_layout.addWidget(x_range_label)
        input_layout.addWidget(self.x_min_input)
        input_layout.addWidget(self.x_max_input)
        input_layout.addWidget(update_button)

        # Create figure and canvas for plotting
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setStyleSheet("background-color: white;")

        # Add matplotlib toolbar
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #181a18;
                color: white;
                border: none;
            }
            QToolButton {
                background-color: #181a18;
                color: white;
                border: none;
            }
            QToolButton:hover {
                background-color: #249c06;
            }
        """)

        # Add widgets to main layout
        layout.addWidget(self.toolbar)
        layout.addWidget(input_widget)
        layout.addWidget(self.canvas)

        # Initial plot if equation is provided
        if self.equation:
            self.update_plot()

    def update_plot(self):
        equation_str = self.equation_input.text()
        if not equation_str:
            QMessageBox.warning(self, "Error", "Please enter an equation!")
            return

        try:
            # Get x range from inputs or use defaults
            x_min = float(self.x_min_input.text()) if self.x_min_input.text() else -10
            x_max = float(self.x_max_input.text()) if self.x_max_input.text() else 10
            
            # Clear the figure
            self.fig.clear()
            ax = self.fig.add_subplot(111)

            # Generate x values and compute y values
            x = np.linspace(x_min, x_max, 1000)
            
            # Create function from string
            def equation_function(x):
                # Replace common mathematical functions
                eq = equation_str.replace('^', '**')
                eq = eq.replace('e', 'np.e')
                eq = eq.replace('sin', 'np.sin')
                eq = eq.replace('cos', 'np.cos')
                eq = eq.replace('tan', 'np.tan')
                eq = eq.replace('exp', 'np.exp')
                eq = eq.replace('log', 'np.log')
                return eval(eq, {"x": x, "np": np})

            y = equation_function(x)

            # Plot the function
            ax.plot(x, y, linewidth=2, color='#2196F3')
            
            # Style the plot
            ax.set_title(f"Plot of {equation_str}", fontsize=14, pad=20)
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('y', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Set the axes to cross at origin if it's in the viewing range
            if x_min <= 0 <= x_max:
                ax.spines['left'].set_position('zero')
            if min(y) <= 0 <= max(y):
                ax.spines['bottom'].set_position('zero')
            
            # Hide the top and right spines
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            
            # Set background colors
            ax.set_facecolor('#f5f5f5')
            self.fig.patch.set_facecolor('white')
            
            # Update the canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error plotting equation: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())