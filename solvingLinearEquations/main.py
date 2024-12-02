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
        self.sig_slider.setRange(1, 20)
        self.sig_slider.setValue(self.significant_figures)
        self.sig_slider.valueChanged.connect(self.Change_Precision)
        

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
        self.Num_input = QLineEdit(self)
        self.Num_input.setPlaceholderText("Enter Number of Iterations: ")
        self.Error_input = QLineEdit(self)
        self.Error_input.setPlaceholderText("Enter the Error Value: ")
        self.Error_input.setVisible(False)
        self.Max_input = QLineEdit(self)
        self.Max_input.setPlaceholderText("Enter the Maximum Number of Iterations: ")
        self.Max_input.setVisible(False)
        self.initial_guess = QLineEdit(self)
        self.initial_guess.setPlaceholderText("Enter the value of the initial guess: ")
        self.Num_input.setVisible(False)  # Hide initially
        self.initial_guess.setVisible(False)

    

    # Add the new groups to the main layout
        layout.addWidget(self.limit_radio_group2)
        layout.addWidget(self.limit_radio_group2)
        layout.addWidget(self.Num_input)
        layout.addWidget(self.Error_input)
        layout.addWidget(self.Max_input)
        layout.addWidget(self.initial_guess)

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
        for i in range(50):
            self.results_label.append(QLabel(f"the result in the {i} iteration is "))
            self.results_label[i].setVisible(False)
            layout.addWidget(self.results_label[i])
        self.results_time = QLabel("Time taken")
        layout.addWidget(self.results_time)
        clear_back_button = QPushButton("Clear and Return to Input")
        clear_back_button.clicked.connect(self.on_clear_back_button_click)  # Connect to the new method
        Return_To_Last_button = QPushButton("Return to the last inputs")
        Return_To_Last_button.clicked.connect(self.return_back)
        layout.addWidget(clear_back_button)
        layout.addWidget(Return_To_Last_button)

    def on_clear_back_button_click(self):
        self.show_input_page()
        self.clear_inputs()
    def return_back(self):
        self.show_input_page()
        self.get_last_update()
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
            self.Num_input.setVisible(False)  # Hide initially
            self.Error_input.setVisible(False)
            self.Max_input.setVisible(False)
            self.initial_guess.setVisible(False)
        elif(method == 'LU Decomposition'):
            QMessageBox.information(self, "Method Selected", f"You selected: {method}")
            self.radio_group1.setVisible(True)  # Hide radio buttons
            self.limit_radio_group2.setVisible(False)  # Hide radio buttons
            self.Num_input.setVisible(False)  # Hide initially
            self.Error_input.setVisible(False)
            self.Max_input.setVisible(False)
            self.initial_guess.setVisible(False)
        else:
            QMessageBox.information(self, "Method Selected", f"You selected: {method}")
            self.radio_group1.setVisible(False)  # Hide radio buttons
            self.limit_radio_group2.setVisible(True)  # Hide radio buttons
            self.radio_ite.toggled.connect(self.Appear_number)
            self.radio_error.toggled.connect(self.Appear_Error)                
            self.initial_guess.setVisible(True)
    def Appear_number(self):
        self.Num_input.setVisible(True)  # Hide initially
        self.Error_input.setVisible(False)
        self.Max_input.setVisible(False)
    def Appear_Error(self):
        self.Num_input.setVisible(False)  # Hide initially
        self.Error_input.setVisible(True)
        self.Max_input.setVisible(True)

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
        ans_string = 'the answer'
        if method == 'Gauss Elimination':
            gauss_solver = Gauss(self.data)
            ans = gauss_solver.solve(precision = self.significant_figures)
            t = gauss_solver.getTime()
            ans_string = gauss_solver.toString()
        elif method == 'Gauss-Jordan':
            jordan_solver = Jordan(self.data)
            ans = jordan_solver.solve(precision = self.significant_figures)
            t = jordan_solver.getTime()
            ans_string = jordan_solver.toString()
        elif method == 'LU Decomposition':
            LU_solver = LU(self.data)
            if self.radio_button1.isChecked():
                ans = LU_solver.solve_doolittle(precision = self.significant_figures)
            elif self.radio_button2.isChecked():
                ans = LU_solver.solve_crout(precision = self.significant_figures)
            elif self.radio_button3.isChecked():
                ans = LU_solver.solve_cholesky(precision = self.significant_figures)
            t = LU_solver.getTime()
            ans_string = LU_solver.toString()
        elif method == 'Gauss-Seidel':
            seidel_solver = Seidel(self.data)
            if self.radio_ite.isChecked() :
                ans = seidel_solver.solve(iterations=int(self.Num_input.text()),initial=int(self.initial_guess.text()), precision = self.significant_figures)
            elif self.radio_error.isChecked() :
                ans = seidel_solver.solve(error=float(self.Error_input.text()),initial=int(self.initial_guess.text()),max_iteration = int(self.Max_input.text()), precision = self.significant_figures)
            t = seidel_solver.getTime()
            ans_string = seidel_solver.toString()
        else:
            Jacobi_solver = Jacobi(self.data)
            if self.radio_ite.isChecked() :
                ans = Jacobi_solver.solve(iterations=int(self.Num_input.text()),initial=int(self.initial_guess.text()), precision = self.significant_figures)
            elif self.radio_error.isChecked() :
                ans = Jacobi_solver.solve(error=float(self.Error_input.text()),initial=int(self.initial_guess.text()),max_iteration = int(self.Max_input.text()), precision = self.significant_figures)
            t = Jacobi_solver.getTime()
            ans_string = Jacobi_solver.toString()

        self.results_label[0].setText(f"{ans_string}")  # Add to the list
        self.results_label[0].setVisible(True)

# Assuming you have a layout to set the results layout to


        self.results_time.setText(f"Execution time : {t}")
        self.stacked_widget.setCurrentWidget(self.results_page)

    def show_input_page(self):
        self.stacked_widget.setCurrentWidget(self.input_page)

    def start(self):
        method = self.method_combo.currentText()  # Get the selected method
        self.solve(method)  # Call the solve method
    def clear_inputs(self):
        self.variables = 2
        self.significant_figures = 3
        self.var_slider.setValue(self.variables)
        self.sig_slider.setValue(self.significant_figures)
        self.data = Data(a=[], b=[])
        for i in range(self.variables):
            for j in range(self.variables):
                item = self.equation_grid.itemAt(i * (self.variables * 2 + 1) + j * 2)
                if item is not None:  # Check if the item exists
                    widget = item.widget()  # Get the widget
                    if widget is not None:  # Check if the widget is valid
                        widget.setText("")  # Clear the text
            if(i%2==0):
                clearing_item = self.equation_grid.itemAt((i+1)*(self.variables*2))
                if clearing_item is not None:  # Check if the item exists
                    widget = clearing_item.widget()  # Get the widget
                    if widget is not None:  # Check if the widget is valid
                        widget.setText("")  # Clear the text
            else:
                clearing_item = self.equation_grid.itemAt((i+1)*(self.variables*2) + 1)
                if clearing_item is not None:  # Check if the item exists
                    widget = clearing_item.widget()  # Get the widget
                    if widget is not None:  # Check if the widget is valid
                        widget.setText("")
        self.radio_ite.setChecked(True)
        self.limit_input.setText("")
        self.initial_guess.setText("")
    def get_last_update(self):
        self.data = Data(a=[], b=[])

    
    def Change_Precision(self):
        self.significant_figures = self.sig_slider.value()

    def end(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EquationSolverApp()
    ex.show()
    sys.exit(app.exec_())