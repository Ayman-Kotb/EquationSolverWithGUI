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
    QLineEdit, QSlider, QPushButton, QMessageBox, QGridLayout, QComboBox, QRadioButton, QGroupBox, QStackedWidget,
    QScrollArea
)
from PyQt5.QtCore import pyqtSignal

class EquationSolverApp(QWidget):
    return_to_main = pyqtSignal()
    open_non_linear_solver = pyqtSignal()

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
        self.setStyleSheet("background-color: #0d0d0d;")

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
        var_label.setStyleSheet("""
            QLabel{
                color: #ccc;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.var_slider = QSlider()
        self.var_slider.setOrientation(1)  # Horizontal
        self.var_slider.setRange(2, 15)
        self.var_slider.setValue(self.variables)
        self.var_slider.valueChanged.connect(self.update_equation_rows)
        self.var_slider.setStyleSheet("""
            QSlider {
                height: 25px;      /* Thickness of the slider */
            }
            QSlider::handle {
                background: #0e5406;  /* Color of the handle */
                width: 10px;       /* Width of the handle */
                margin: -10px 0;    /* Center the handle */
                border-radius: 10px; /* Rounded handle */
            }
            QSlider::handle:pressed {
                background: #0b3001;  /* Color of the handle when pressed */
            }
            QSlider::groove {
                background: #181a18;  /* Color of the groove */
                height: 5px;       /* Thickness of the groove */
            }
        """)

        var_layout.addWidget(var_label)
        var_layout.addWidget(self.var_slider)
        layout.addLayout(var_layout)

        # Significant Figures
        sig_layout = QHBoxLayout()
        sig_label = QLabel("Significant Figures:")
        sig_label.setStyleSheet("""
            QLabel{
                color: #ccc;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.sig_slider = QSlider()
        self.sig_slider.setOrientation(1)  # Horizontal
        self.sig_slider.setRange(1, 20)
        self.sig_slider.setValue(self.significant_figures)
        self.sig_slider.valueChanged.connect(self.Change_Precision)
        self.sig_slider.setStyleSheet("""
            QSlider {
                height: 25px;      /* Thickness of the slider */
            }
            QSlider::handle {
                background: #0e5406;  /* Color of the handle */
                width: 10px;       /* Width of the handle */
                margin: -10px 0;    /* Center the handle */
                border-radius: 20px; /* Rounded handle */
            }
            QSlider::handle:pressed {
                background: #0b3001;  /* Color of the handle when pressed */
            }
            QSlider::groove {
                background: #181a18;  /* Color of the groove */
                height: 5px;       /* Thickness of the groove */
            }
        """)
        self.sig_current = QLabel(f": {self.significant_figures}")
        self.sig_current.setFixedHeight(20)
        self.sig_current.setFixedWidth(35)
        self.sig_current.setStyleSheet("""
            QLabel{
                background: #181a18;
                color: #ccc;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        sig_layout.addWidget(sig_label)
        sig_layout.addWidget(self.sig_slider)
        sig_layout.addWidget(self.sig_current)
        layout.addLayout(sig_layout)

        # Equation Input
        self.equation_grid = QGridLayout()
        self.equations = []
        self.create_equation_rows()
        layout.addLayout(self.equation_grid)

        # Method Selection
        method_layout = QHBoxLayout()
        method_label = QLabel("Select Method:")
        method_label.setStyleSheet("""
            QLabel{
                color: #ccc;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.method_combo = QComboBox()
        methods = ["Gauss Elimination", "Gauss-Jordan", "LU Decomposition", "Gauss-Seidel", "Jacobi-Iteration"]
        self.method_combo.addItems(methods)
        self.method_combo.currentIndexChanged.connect(self.method_selected)
        self.method_combo.setStyleSheet("""
            QComboBox {
                background-color: #181a18;  /* Background color */
                color: white;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 14px;
                font-weight: bold;
                }
            QComboBox::drop-down {
                border: 2px solid #ccc;      /* Border of the drop-down area */
                border-radius: 10px;         /* Rounded borders for the drop-down */
                width: 20px;                  /* Width of the drop-down arrow area */
            }
             QComboBox QAbstractItemView {
                background-color: #181a18;
                selection-background-color: #55e339; /* Background color on hover */
                selection-color: #ccc; /* Text color on hover */
            }
            QComboBox QAbstractItemView::item {
                background-color: #181a18; /* Default item background */
                color: #ccc; /* Default item text color */
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #55e339; /* Background color when hovering */
                color: #ccc; /* Text color when hovering */
            }      
        """)

        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        layout.addLayout(method_layout)


        self.radio_group1 = QGroupBox("Select LU Decomposition Method")
        self.radio_group1.setStyleSheet("""
                QGroupBox{
                    color: white;                /* Text color */
                    font-size: 14px;
                    font-weight: bold;
                }
        """)
        self.radio_layout = QHBoxLayout()
    
        self.radio_button1 = QRadioButton("Doolittle Form")
        self.radio_button1.setStyleSheet("""
                QRadioButton{
                    color: white;                /* Text color */
                    font-size: 14px;
                    font-weight: bold;
                }
                 QRadioButton::indicator {
                width: 10px; /* Width of the radio button */
                height: 10px; /* Height of the radio button */
                border: 2px solid #b80404; /* Border color when unselected */
                border-radius: 5px; /* Rounded edges */
                background-color: #ccc; /* Background color */
                }
                QRadioButton::indicator:checked {
                background-color: #b80404; /* Background when selected */
                border: 2px solid #b80404; /* Border color when selected */
                }
                QRadioButton::indicator:hover{
                    background-color: #870808;
                    border: 2px solid #870808;
                }
        """)
        self.radio_button2 = QRadioButton("Crout Form")
        self.radio_button2.setStyleSheet("""
                QRadioButton{
                    color: white;                /* Text color */
                    font-size: 14px;
                    font-weight: bold;
                }
                 QRadioButton::indicator {
                width: 10px; /* Width of the radio button */
                height: 10px; /* Height of the radio button */
                border: 2px solid #b80404; /* Border color when unselected */
                border-radius: 5px; /* Rounded edges */
                background-color: #ccc; /* Background color */
                }
                QRadioButton::indicator:checked {
                background-color: #b80404; /* Background when selected */
                border: 2px solid #b80404; /* Border color when selected */
                }
                QRadioButton::indicator:hover{
                    background-color: #870808;
                    border: 2px solid #870808;
                }
        """)
        self.radio_button3 = QRadioButton("Cholesky Form")
        self.radio_button3.setStyleSheet("""
                QRadioButton{
                    color: white;                /* Text color */
                    font-size: 14px;
                    font-weight: bold;
                }
                 QRadioButton::indicator {
                width: 10px; /* Width of the radio button */
                height: 10px; /* Height of the radio button */
                border: 2px solid #b80404; /* Border color when unselected */
                border-radius: 5px; /* Rounded edges */
                background-color: #ccc; /* Background color */
                }
                QRadioButton::indicator:checked {
                background-color: #b80404; /* Background when selected */
                border: 2px solid #b80404; /* Border color when selected */
                }
                QRadioButton::indicator:hover{
                    background-color: #870808;
                    border: 2px solid #870808;
                }
        """)
    
        self.radio_layout.addWidget(self.radio_button1)
        self.radio_layout.addWidget(self.radio_button2)
        self.radio_layout.addWidget(self.radio_button3)
        self.radio_group1.setLayout(self.radio_layout)
        self.radio_group1.setVisible(False)  # Hide initially
    
    # Add the radio button group to the main layout
        layout.addWidget(self.radio_group1)

        self.limit_radio_group2 = QGroupBox("Select Iteration Method")
        self.limit_radio_group2.setStyleSheet("""
            QGroupBox{
                color: white;                /* Text color */
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.limit_radio_layout = QHBoxLayout()  # Arrange horizontally

        self.radio_ite = QRadioButton("Using Number of Iterations")
        self.radio_ite.setStyleSheet("""
                QRadioButton{
                    color: white;                /* Text color */
                    font-size: 14px;
                    font-weight: bold;
                }
                 QRadioButton::indicator {
                width: 10px; /* Width of the radio button */
                height: 10px; /* Height of the radio button */
                border: 2px solid #b80404; /* Border color when unselected */
                border-radius: 5px; /* Rounded edges */
                background-color: #ccc; /* Background color */
                }
                QRadioButton::indicator:checked {
                background-color: #b80404; /* Background when selected */
                border: 2px solid #b80404; /* Border color when selected */
                }
                QRadioButton::indicator:hover{
                    background-color: #870808;
                    border: 2px solid #870808;
                }
        """)
        self.radio_error = QRadioButton("Using Absolute Relative Error")
        self.radio_error.setStyleSheet("""
                QRadioButton{
                    color: white;                /* Text color */
                    font-size: 14px;
                    font-weight: bold;
                }
                 QRadioButton::indicator {
                width: 10px; /* Width of the radio button */
                height: 10px; /* Height of the radio button */
                border: 2px solid #b80404; /* Border color when unselected */
                border-radius: 5px; /* Rounded edges */
                background-color: #ccc; /* Background color */
                }
                QRadioButton::indicator:checked {
                background-color: #b80404; /* Background when selected */
                border: 2px solid #b80404; /* Border color when selected */
                }
                QRadioButton::indicator:hover{
                    background-color: #870808;
                    border: 2px solid #870808;
                }
        """)
        self.limit_radio_layout.addWidget(self.radio_ite)
        self.limit_radio_layout.addWidget(self.radio_error)

        self.limit_radio_group2.setLayout(self.limit_radio_layout)
        self.limit_radio_group2.setVisible(False)  # Hide initially
        self.Num_input = QLineEdit(self)
        self.Num_input.setStyleSheet("""
            QLineEdit {
                background-color: #181a18;  /* Background color */
                color: white;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.Num_input.setPlaceholderText("Enter Number of Iterations: ")
        self.Error_input = QLineEdit(self)
        self.Error_input.setPlaceholderText("Enter the Error Value: ")
        self.Error_input.setStyleSheet("""
            QLineEdit {
                background-color: #181a18;  /* Background color */
                color: white;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.Error_input.setVisible(False)
        self.Max_input = QLineEdit(self)
        self.Max_input.setPlaceholderText("Enter the Maximum Number of Iterations: ")
        self.Max_input.setStyleSheet("""
            QLineEdit {
                background-color: #181a18;  /* Background color */
                color: white;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.Max_input.setVisible(False)
        self.initial_guess = QLineEdit(self)
        self.initial_guess.setPlaceholderText("Enter the value of the initial guess: ")
        self.initial_guess.setStyleSheet("""
            QLineEdit {
                background-color: #181a18;  /* Background color */
                color: white;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 20px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
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
        start_button.setStyleSheet("""
            QPushButton{
                background-color: #181a18;  /* Background color */
                color: #249c06;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #249c06;   /* Background color on hover */
                color: #ccc;
                border: 2px solid #249c06;
            }
        """)

        end_button = QPushButton("End")
        end_button.clicked.connect(self.end) # ebn
        control_layout.addWidget(end_button)
        end_button.setStyleSheet("""
            QPushButton{
                background-color: #181a18;  /* Background color */
                color: #b80404;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b80404;   /* Background color on hover */
                color: #ccc;
                border: 2px solid #b80404;
            }
        """)

        layout.addLayout(control_layout)

        Switching_layout = QHBoxLayout()
        linear_switch_button = QPushButton("Switch to Non-Linear Equations")
        linear_switch_button.clicked.connect(self.open_non_linear_window)
        Switching_layout.addWidget(linear_switch_button)
        linear_switch_button.setStyleSheet("""
                QPushButton{
                background-color: #181a18;  /* Background color */
                color: #5b24a3;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5b24a3;   /* Background color on hover */
                color: #ccc;
                border: 2px solid #5b24a3;
            }
            """)
        
        back_main_button = QPushButton("Return Back to Main Page")
        back_main_button.clicked.connect(self.open_main_window)
        Switching_layout.addWidget(back_main_button)
        back_main_button.setStyleSheet("""
               QPushButton {
            background-color: #181a18;  /* Background color */
            color: #e8c113;             /* Text color */
            border: 2px solid #181a18;  /* Border color and width */
            border-radius: 10px;        /* Rounded borders */
            padding: 5px;               /* Optional padding */
            height: 15px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8c113;  /* Background color on hover */
            color: #ccc;
            border: 2px solid #e8c113;
        }
            """)
        
        layout.addLayout(Switching_layout)

    def setup_results_page(self, layout):
    # Main layout for the results
        main_layout = QVBoxLayout()

    # Result label
        self.results_label = QLabel("The result is: " + "This is a very long result that needs to be scrollable. " * 50)
        self.results_label.setStyleSheet("""
        QLabel {
            color: white;                /* Text color */
            font-size: 13px;
            font-weight: bold;
        }
    """)
        self.results_label.setWordWrap(True)  # Enable word wrap

    # Scroll area beside the results label
        self.scroll_area_beside = QScrollArea()
        self.scroll_area_beside.setWidgetResizable(True)
    
    # Set the results label as the widget for the scroll area
        self.scroll_area_beside.setWidget(self.results_label)

    # Horizontal layout for results label and scroll area
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.scroll_area_beside)

    # Add horizontal layout to the main layout
        main_layout.addLayout(h_layout)

    # Time taken label
        self.results_time = QLabel("Time taken")
        self.results_time.setStyleSheet("""
        QLabel {
            color: white;                /* Text color */
            font-size: 13px;
            font-weight: bold;
        }
    """)
        main_layout.addWidget(self.results_time)

    # Buttons
        clear_back_button = QPushButton("Clear and Return to Input")
        clear_back_button.clicked.connect(self.on_clear_back_button_click)
        clear_back_button.setStyleSheet("""
        QPushButton {
            background-color: #181a18;  /* Background color */
            color: #b80404;             /* Text color */
            border: 2px solid #181a18;  /* Border color and width */
            border-radius: 10px;        /* Rounded borders */
            padding: 5px;               /* Optional padding */
            height: 15px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #b80404;  /* Background color on hover */
            color: #ccc;
            border: 2px solid #b80404;
        }
    """)
    
        Return_To_Last_button = QPushButton("Return to the last inputs")
        Return_To_Last_button.clicked.connect(self.return_back)
        Return_To_Last_button.setStyleSheet("""
        QPushButton {
            background-color: #181a18;  /* Background color */
            color: #e8c113;             /* Text color */
            border: 2px solid #181a18;  /* Border color and width */
            border-radius: 10px;        /* Rounded borders */
            padding: 5px;               /* Optional padding */
            height: 15px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e8c113;  /* Background color on hover */
            color: #ccc;
            border: 2px solid #e8c113;
        }
    """)

    # Add buttons to the main layout
        main_layout.addWidget(clear_back_button)
        main_layout.addWidget(Return_To_Last_button)

    # Set the layout for the parent widget
        layout.addLayout(main_layout)

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
            entry_var.setFixedWidth(60)
            self.equation_grid.addWidget(entry_var, row, var_index)
            entry_var.setStyleSheet("""
                QLineEdit {
                background-color: #181a18;  /* Background color */
                color: white;                /* Text color */
                border: 2px solid #181a18;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 12px;
                font-weight: bold;
                }
            """)

            if var_index != 2 * self.variables - 2:
                label_var = QLabel(f"x{var_index // 2 + 1} + ")
                self.equation_grid.addWidget(label_var, row, var_index + 1)
                label_var.setStyleSheet("""
                QLabel{
                    color: #ccc;
                    font-size: 14px;
                    font-weight: bold;
                }
                """)
            else:
                label_var = QLabel(f"x{var_index // 2 + 1} = ")
                self.equation_grid.addWidget(label_var, row, var_index + 1)
                label_var.setStyleSheet("""
                QLabel{
                    color: #ccc;
                    font-size: 14px;
                    font-weight: bold;
                }
                """)

        entry_res = QLineEdit(self)
        entry_res.setFixedWidth(60)
        self.equation_grid.addWidget(entry_res, row, self.variables * 2 + 1)
        entry_res.setStyleSheet("""
            QLineEdit {
            background-color: #181a18;  /* Background color */
            color: white;                /* Text color */
            border: 2px solid #181a18;      /* Border color and width */
            border-radius: 10px;         /* Rounded borders */
            padding: 5px;                /* Optional padding */
            height: 15px;
            font-size: 12px;
            font-weight: bold;
            }
        """)

        self.equations.append(entry_res)  # Store the result entry for later use

    def update_equation_rows(self):
        self.variables = self.var_slider.value()
        self.create_equation_rows()  # Update the equation rows

    def method_selected(self):
        method = self.method_combo.currentText()
        if(method == 'Gauss Elimination' or method == 'Gauss-Jordan'):
            self.radio_group1.setVisible(False)  # Hide radio buttons
            self.limit_radio_group2.setVisible(False)  # Hide radio buttons
            self.Num_input.setVisible(False)  # Hide initially
            self.Error_input.setVisible(False)
            self.Max_input.setVisible(False)
            self.initial_guess.setVisible(False)
        elif(method == 'LU Decomposition'):
            self.radio_group1.setVisible(True)  # Hide radio buttons
            self.limit_radio_group2.setVisible(False)  # Hide radio buttons
            self.Num_input.setVisible(False)  # Hide initially
            self.Error_input.setVisible(False)
            self.Max_input.setVisible(False)
            self.initial_guess.setVisible(False)
        else:
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
            constant_entry = self.equation_grid.itemAt((i+1)*(self.variables*2) + i).widget().text()
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
                ans = seidel_solver.solve(iterations=int(self.Num_input.text()),initial=float(self.initial_guess.text()), precision = self.significant_figures)
            elif self.radio_error.isChecked() :
                ans = seidel_solver.solve(error=float(self.Error_input.text()),initial=float(self.initial_guess.text()),max_iteration = int(self.Max_input.text()), precision = self.significant_figures)
            t = seidel_solver.getTime()
            ans_string = seidel_solver.toString()
        else:
            Jacobi_solver = Jacobi(self.data)
            if self.radio_ite.isChecked() :
                ans = Jacobi_solver.solve(iterations=int(self.Num_input.text()),initial=float(self.initial_guess.text()), precision = self.significant_figures)
            elif self.radio_error.isChecked() :
                ans = Jacobi_solver.solve(error=float(self.Error_input.text()),initial=float(self.initial_guess.text()),max_iteration = int(self.Max_input.text()), precision = self.significant_figures)
            t = Jacobi_solver.getTime()
            ans_string = Jacobi_solver.toString()

        self.results_label.setText(f"{ans_string}")  # Add to the list
        self.results_label.setVisible(True)

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
        self.Num_input.setText("")
        self.Error_input.setText("")
        self.Max_input.setText("")
        self.initial_guess.setText("")
    def get_last_update(self):
        self.data = Data(a=[], b=[])

    
    def Change_Precision(self):
        self.significant_figures = self.sig_slider.value()
        self.sig_current.setText(f": {self.significant_figures}")

    def end(self):
        QApplication.quit()

    def open_non_linear_window(self):
        self.open_non_linear_solver.emit()
        self.close()

    def open_main_window(self):
        self.return_to_main.emit()
        self.close()
