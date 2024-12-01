import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, \
    QPushButton, QSlider, QComboBox, QMessageBox


class EquationSolverApp(QWidget):
    def __init__(self):
        super().__init__()

        self.variables = 2  # Default number of variables
        self.significant_figures = 2  # Default significant figures

        self.initUI()

    def initUI(self):
        self.setWindowTitle("System of Equations Solver")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        # Number of Variables
        var_layout = QHBoxLayout()
        var_label = QLabel("Number of Variables:")
        self.var_slider = QSlider()
        self.var_slider.setOrientation(1)  # Horizontal
        self.var_slider.setRange(2, 10)
        self.var_slider.setValue(self.variables)
        self.var_slider.valueChanged.connect(self.update_equation_rows)

        var_layout.addWidget(var_label)
        var_layout.addWidget(self.var_slider)
        layout.addLayout(var_layout)

        # Significant Figures
        sig_layout = QHBoxLayout()
        sig_label = QLabel("Significant Figures:")
        self.sig_slider = QSlider()
        self.sig_slider.setOrientation(1)  # Horizontal
        self.sig_slider.setRange(1, 10)
        self.sig_slider.setValue(self.significant_figures)

        sig_layout.addWidget(sig_label)
        sig_layout.addWidget(self.sig_slider)
        layout.addLayout(sig_layout)

        # Equation Input
        self.equation_grid = QGridLayout()
        self.equations = []
        self.create_equation_rows()
        layout.addLayout(self.equation_grid)

        # Method Selection
        method_layout = QHBoxLayout()
        method_label = QLabel("Select Method:")
        self.method_combo = QComboBox()
        methods = ["Gauss Elimination", "Gauss-Jordan", "LU Decomposition", "Gauss-Seidel", "Jacobi-Iteration"]
        self.method_combo.addItems(methods)
        self.method_combo.currentIndexChanged.connect(self.method_selected)

        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        layout.addLayout(method_layout)

        # Control Buttons
        control_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start)
        control_layout.addWidget(start_button)

        end_button = QPushButton("End")
        end_button.clicked.connect(self.end)
        control_layout.addWidget(end_button)

        layout.addLayout(control_layout)

        self.setLayout(layout)

    def create_equation_rows(self):
        # Clear existing equation rows
        for i in reversed(range(self.equation_grid.count())):
            widget = self.equation_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Safely delete the widget

        self.equations.clear()  # Clear the previous equations list

        # Create new equation rows based on the number of variables
        for row in range(self.variables):
            self.create_equation_row(row)

    def create_equation_row(self, row):
        # Create entries for coefficients and the constant
        for var_index in range(0, 2 * self.variables - 1, 2):
            entry_var = QLineEdit(self)
            entry_var.setFixedWidth(40)
            self.equation_grid.addWidget(entry_var, row, var_index)

            if var_index != 2 * self.variables - 2:
                label_var = QLabel(f"x{var_index // 2 + 1} + ")
                self.equation_grid.addWidget(label_var, row, var_index + 1)
            else:
                label_var = QLabel(f"x{var_index // 2 + 1} = ")
                self.equation_grid.addWidget(label_var, row, var_index + 1)

        entry_res = QLineEdit(self)
        entry_res.setFixedWidth(40)
        self.equation_grid.addWidget(entry_res, row, self.variables * 2 + 1)

        self.equations.append(entry_res)  # Store the result entry for later use

    def update_equation_rows(self):
        self.variables = self.var_slider.value()
        self.create_equation_rows()  # Update the equation rows

    def method_selected(self):
        selected_method = self.method_combo.currentText()
        QMessageBox.information(self, "Method Selected", f"You selected: {selected_method}")

    def solve(self, method):
        coefficients = []
        for i in range(len(self.equations)):
            coeffs = [self.equation_grid.itemAt(i * (self.variables * 2 + 1) + j).widget().text()
                      for j in range(self.variables * 2 + 1)]
            coefficients.append(coeffs)

        if any(not coeff for coeff in coefficients):
            QMessageBox.warning(self, "Input Error", "Please fill all coefficients.")
            return

        QMessageBox.information(self, "Method Selected",
                                f"Solving using {method} method with {self.significant_figures} significant figures.\nCoefficients: {coefficients}")

    def start(self):
        QMessageBox.information(self, "Start", "Starting the solver.")

    def end(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EquationSolverApp()
    ex.show()
    sys.exit(app.exec_())
