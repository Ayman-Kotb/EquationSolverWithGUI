import sys
from Gauss import Gauss
from Jordan import Jordan
from Jacobi import Jacobi
from LU import LU
from Seidel import Seidel
from LinearSolution import LinearSolution
from Data import Data
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSlider, QPushButton, QMessageBox, QGridLayout, QComboBox, QRadioButton, QGroupBox, QStackedWidget
)

class EquationSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.data = Data(a=[], b=[])
        self.variables = 2  # Default number of variables
        self.significant_figures = 2  # Default significant figures
        self.a = []  # Matrix to hold coefficients

        self.initUI()

    def initUI(self):
        self.setWindowTitle("System of Equations Solver")
        self.setGeometry(100, 100, 600, 500)

        # Create a stacked widget
        self.stacked_widget = QStackedWidget()
        self.input_page = QWidget()
        self.results_page = QWidget()
        
        # Set up input page layout
        layout = QVBoxLayout()
        self.setup_input_page(layout)
        self.input_page.setLayout(layout)

        # Set up results page layout
        results_layout = QVBoxLayout()
        self.setup_results_page(results_layout)
        self.results_page.setLayout(results_layout)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.results_page)

        # Add the stacked widget to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.radio_group1 = QGroupBox("Select LU Decomposition Method")
        self.radio_layout = QHBoxLayout()
    
        self.radio_button1 = QRadioButton("Doolittle Form")
        self.radio_button2 = QRadioButton("Crout Form")
        self.radio_button3 = QRadioButton("Cholesky Form")

    
        self.radio_layout.addWidget(self.radio_button1)
        self.radio_layout.addWidget(self.radio_button2)
        self.radio_layout.addWidget(self.radio_button3)
        self.radio_group1.setLayout(self.radio_layout)
        self.radio_group1.setVisible(False)  # Hide initially
    
    # Add the radio button group to the main layout
        layout.addWidget(self.radio_group1)

        self.limit_radio_group2 = QGroupBox("Select Iteration Method")
        self.limit_radio_layout = QHBoxLayout()  # Arrange horizontally

        self.radio_ite = QRadioButton("Using Number of Iterations")
        self.radio_error = QRadioButton("Using Absolute Relative Error")

        self.limit_radio_layout.addWidget(self.radio_ite)
        self.limit_radio_layout.addWidget(self.radio_error)

        self.limit_radio_group2.setLayout(self.limit_radio_layout)
        self.limit_radio_group2.setVisible(False)  # Hide initially
        self.limit_input = QLineEdit(self)
        self.limit_input.setPlaceholderText("Enter limit value: ")
        self.initial_guess = QLineEdit(self)
        self.initial_guess.setPlaceholderText("Enter the value of the initial guess: ")
        self.limit_input.setVisible(False)  # Hide initially
        self.initial_guess.setVisible(False)

    

    # Add the new groups to the main layout
        layout.addWidget(self.limit_radio_group2)
        layout.addWidget(self.limit_radio_group2)
        layout.addWidget(self.limit_input)
        layout.addWidget(self.initial_guess)


    def setup_input_page(self, layout):
        # Number of Variables
        var_layout = QHBoxLayout()
        var_label = QLabel("Number of Variables:")
        self.var_slider = QSlider()
        self.var_slider.setOrientation(1)  # Horizontal
        self.var_slider.setRange(2, 15)
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

    def setup_results_page(self, layout):
        self.results_label = []
        for i in range(10):
            self.results_label.append(QLabel(f"the result in the {i} iteration is "))
            self.results_label[i].setVisible(False)
            layout.addWidget(self.results_label[i])
        self.results_time = QLabel("Time taken")
        layout.addWidget(self.results_time)
        back_button = QPushButton("Back to Input")
        back_button.clicked.connect(self.show_input_page)
        layout.addWidget(back_button)

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
        method = self.method_combo.currentText()
        if(method == 'Gauss Elimination' or method == 'Gauss-Jordan'):
            QMessageBox.information(self, "Method Selected", f"You selected: {method}")
            self.radio_group1.setVisible(False)  # Hide radio buttons
            self.limit_radio_group2.setVisible(False)  # Hide radio buttons
            self.limit_input.setVisible(False)  # Hide initially
            self.initial_guess.setVisible(False)
        elif(method == 'LU Decomposition'):
            QMessageBox.information(self, "Method Selected", f"You selected: {method}")
            self.radio_group1.setVisible(True)  # Hide radio buttons
            self.limit_radio_group2.setVisible(False)  # Hide radio buttons
            self.limit_input.setVisible(False)  # Hide initially
            self.initial_guess.setVisible(False)
        else:
            QMessageBox.information(self, "Method Selected", f"You selected: {method}")
            self.radio_group1.setVisible(False)  # Hide radio buttons
            self.limit_radio_group2.setVisible(True)  # Hide radio buttons
            self.limit_input.setVisible(True)  # Hide initially
            self.initial_guess.setVisible(True)

    def solve(self, method):
        for i in range(self.variables):
            row = []  # Create a new row for the coefficients
            for j in range(self.variables):
                coeff_entry = self.equation_grid.itemAt(i * (self.variables * 2 + 1) + j * 2).widget().text()
                row.append(float(coeff_entry))  # Convert the input to float and add to the row
            self.data.a.append(row)
            if(i%2==0):
                constant_entry = self.equation_grid.itemAt((i+1)*(self.variables*2)).widget().text()
            else:
                constant_entry = self.equation_grid.itemAt((i+1)*(self.variables*2) + 1).widget().text()
            self.data.b.append(float(constant_entry))  # Append the row to the matrix
        
        # Solve using the selected method
        t = 0
        if method == 'Gauss Elimination':
            gauss_solver = Gauss(self.data)
            ans = gauss_solver.solve()
            t = gauss_solver.getTime()
        elif method == 'Gauss-Jordan':
            jordan_solver = Jordan(self.data)
            ans = jordan_solver.solve()
            t = jordan_solver.getTime()
        elif method == 'LU Decomposition':
            LU_solver = LU(self.data)
            if self.radio_button1.isChecked():
                ans = LU_solver.solve_doolittle()
            elif self.radio_button2.isChecked():
                ans = LU_solver.solve_crout()
            elif self.radio_button3.isChecked():
                ans = LU_solver.solve_cholesky()
            t = LU_solver.getTime()
        elif method == 'Gauss-Seidel':
            seidel_solver = Seidel(self.data)
            if self.radio_ite.isChecked() :
                ans = seidel_solver.solve(iterations=int(self.limit_input.text()),initial=int(self.initial_guess.text()))
            elif self.radio_error.isChecked() :
                ans = seidel_solver.solve(error=float(self.limit_input.text()),initial=int(self.initial_guess.text()))
            t = seidel_solver.getTime()
        else:
            Jacobi_solver = Jacobi(self.data)
            if self.radio_ite.isChecked() :
                ans = Jacobi_solver.solve(iterations=int(self.limit_input.text()),initial=int(self.initial_guess.text()))
            elif self.radio_error.isChecked() :
                ans = Jacobi_solver.solve(error=float(self.limit_input.text()),initial=int(self.initial_guess.text()))
            t = Jacobi_solver.getTime()

        # Show 
        if method in ['Gauss Elimination', 'Gauss-Jordan', 'LU Decomposition']:
    # Display the overall answer for these methods
            solutions = ans
            self.results_label[0].setText(f"The answer is {solutions.getSolutions()}")  # Add to the list
            self.results_label[0].setVisible(True)
        else:
    # Assuming ans.getSolutions() returns a list of solutions for other methods
            solutions = ans  # Get the list of solutions
            for i in range(len(solutions) - 1):  # Iterate over the solutions
                self.results_label[i].setText(f"The answer of {i + 1} is {solutions[i].getSolutions()}")  # Add to the list
                self.results_label[i].setVisible(True)

# Assuming you have a layout to set the results layout to


        self.results_time.setText(f"Execution time : {t}")
        self.stacked_widget.setCurrentWidget(self.results_page)

    def show_input_page(self):
        self.stacked_widget.setCurrentWidget(self.input_page)

    def start(self):
        method = self.method_combo.currentText()  # Get the selected method
        self.solve(method)  # Call the solve method

    def end(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EquationSolverApp()
    ex.show()
    sys.exit(app.exec_())
