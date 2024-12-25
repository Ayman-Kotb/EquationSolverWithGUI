from Plot import PlotWindow
from Bisection import Bisection
from NewtonRaphson import Original_Newton_Raphson
from Secant import Secant
from ModifiedSecant import ModifiedSecant
from FixedPoint import FixedPoint
from FalsePosition import false_position
from Modified1Newton import Modified1_Newton_Raphson
from Modified2Newton import Modified2_Newton_Raphson
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSlider, QPushButton, QMessageBox, QGridLayout, QComboBox, QRadioButton, QGroupBox, QStackedWidget,
    QScrollArea
)
from PyQt5.QtCore import pyqtSignal
from ErrorHandler import ErrorHandler
import time

import sys
from sympy import symbols, sympify, lambdify
class NonLinearSolver(QWidget):
    return_to_main = pyqtSignal()
    open_equation_solver = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.first = 0
        self.sec = 1 
        self.variables = 2  # Default number of variables
        self.significant_figures = 2  # Default significant figures
        self.equation = ""
        self.result = []
        self.sub_selection = "Secant"
        self.picked = "Bisection"
        self.time = 0
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

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def open_plot_window(self , equation_str):
      # Define the string equation to plot
      equation_str = self.equation_input.text()  # Example string representation of the equation
      
      # Open the plotting window and pass the string equation
      self.plot_window = PlotWindow(
          equation_str=equation_str,  # Pass the string equation here
          x_range=(-5, 5),
          title="Linear Function: f(x) = 3x + 5"
      )
      self.plot_window.show()




    def setup_input_page(self, layout):
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


        self.equation_input = QLineEdit(self)
        self.equation_input.setPlaceholderText("Enter the Equation to be solved: ")
        self.equation_input.setStyleSheet("""
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
        layout.addWidget(self.equation_input)
        
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.open_plot_window)
        #plot_button.clicked.connect()  # Connect to your plot function
        layout.addWidget(plot_button)

        # Style the Plot button with new color scheme
        plot_button.setStyleSheet("""
            QPushButton{
               background-color: #000000;  /* Background color */
                color: #0000FF;                /* Text color */
                border: 2px solid #0000FF;      /* Border color and width */
                border-radius: 10px;         /* Rounded borders */
                padding: 5px;                /* Optional padding */
                height: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0000FF;   /* Background color on hover */
                color: #ccc;
                border: 2px solid #0000FF;
            }
        """)

        
        initial_values_layout = QHBoxLayout()
        self.initial_value_0 = QLineEdit(self)
        self.initial_value_0.setPlaceholderText("Enter the first initial value: ")
        self.initial_value_0.setStyleSheet("""
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

        self.initial_value_1 = QLineEdit(self)
        self.initial_value_1.setPlaceholderText("Enter the second initial value: ")
        self.initial_value_1.setStyleSheet("""
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

        self.initial_value_1.setVisible(True)

        initial_values_layout.addWidget(self.initial_value_0)
        initial_values_layout.addWidget(self.initial_value_1)

        self.m = QLineEdit(self)
        self.m.setPlaceholderText("Enter the m value: ")
        self.m.setStyleSheet("""
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
        self.m.setVisible(False)

        NR_method_layout = QHBoxLayout()
        self.NR_method_label = QLabel("Select Newton - Raphson Version:")
        self.NR_method_label.setStyleSheet("""
            QLabel{
                color: #ccc;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.NR_method_combo = QComboBox()
        NR_methods = ["Original Newton-Raphson", "Modified Version 1 : Newton-Raphson", "Modified Version 2 : Newton-Raphson"]
        self.NR_method_combo.addItems(NR_methods)
        self.NR_method_combo.currentIndexChanged.connect(lambda: self.NR_method_selected(self.NR_method_combo.currentText()))
        self.NR_method_combo.setStyleSheet("""
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

        NR_method_layout.addWidget(self.NR_method_label)
        NR_method_layout.addWidget(self.NR_method_combo)
        self.NR_method_label.setVisible(False)
        self.NR_method_combo.setVisible(False)

        SE_method_layout = QHBoxLayout()
        self.SE_method_label = QLabel("Select Secant Version:")
        self.SE_method_label.setStyleSheet("""
            QLabel{
                color: #ccc;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.SE_method_combo = QComboBox()
        SE_methods = ["Secant Method", "Modified Secant Method"]
        self.SE_method_combo.addItems(SE_methods)
        self.SE_method_combo.currentIndexChanged.connect(lambda: self.SE_method_selected(self.SE_method_combo.currentText()))
        self.SE_method_combo.setStyleSheet("""
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

        SE_method_layout.addWidget(self.SE_method_label)
        SE_method_layout.addWidget(self.SE_method_combo)
        self.SE_method_label.setVisible(False)
        self.SE_method_combo.setVisible(False)

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
        methods = ["Bisection", "False Position","Fixed-Point Iteration", "Newton-Raphson Methods", "Secant Methods"]
        self.method_combo.addItems(methods)
        self.method_combo.currentIndexChanged.connect(lambda: self.method_selected(self.method_combo.currentText()))
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
        layout.addLayout(SE_method_layout)
        layout.addLayout(NR_method_layout)
        layout.addLayout(initial_values_layout)
        layout.addWidget(self.m)

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
        
        layout.addWidget(self.Error_input)

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

        layout.addWidget(self.Max_input)

        control_layout = QHBoxLayout()
        start_button = QPushButton("Start") # Start button
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
        end_button.clicked.connect(self.end)
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
        layout

        Switching_layout = QHBoxLayout()
        linear_switch_button = QPushButton("Switch to Linear Equations")
        linear_switch_button.clicked.connect(self.open_linear_window)
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
        self.results_time = QLabel("Time taken")
        self.results_time.setStyleSheet("""
        QLabel {
            color: white;                /* Text color */
            font-size: 13px;
            font-weight: bold;
        }
    """)
        main_layout.addWidget(self.results_time)
    # Time taken label
        self.results_history = QComboBox()
        self.results_history.setStyleSheet("""
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
        self.results_history.currentIndexChanged.connect(lambda : self.change_result())
        main_layout.addWidget(self.results_history)


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

    def Change_Precision(self):
        self.significant_figures = self.sig_slider.value()
        self.sig_current.setText(f": {self.significant_figures}")

    def method_selected(self, Selection):
        self.picked = Selection
        if((Selection == "Bisection") | (Selection == "False Position")):
            self.initial_value_1.setVisible(True)
            self.NR_method_label.setVisible(False)
            self.SE_method_label.setVisible(False)
            self.SE_method_combo.setVisible(False)
            self.NR_method_combo.setVisible(False)
            self.m.setVisible(False)
        elif(Selection == "Newton-Raphson Methods"):
            self.initial_value_1.setVisible(False)
            self.NR_method_label.setVisible(True)
            self.SE_method_label.setVisible(False)
            self.SE_method_combo.setVisible(False)
            self.NR_method_combo.setVisible(True)
        elif(Selection == "Secant Methods"):
            self.initial_value_1.setVisible(True)
            self.NR_method_label.setVisible(False)
            self.SE_method_label.setVisible(True)
            self.SE_method_combo.setVisible(True)
            self.NR_method_combo.setVisible(False)
            self.m.setVisible(False)
        else:
            self.initial_value_1.setVisible(False)
            self.NR_method_label.setVisible(False)
            self.SE_method_label.setVisible(False)
            self.SE_method_combo.setVisible(False)
            self.NR_method_combo.setVisible(False)
            self.m.setVisible(False)

    def SE_method_selected(self, Selection):
        if(Selection == "Secant Method"):
            self.initial_value_1.setPlaceholderText("Enter the second initial value: ")
            self.sub_selection = "Secant"
        else:
            self.initial_value_1.setPlaceholderText("Enter the delta value: ")
            self.sub_selection = "Modified Secant"
    
    def NR_method_selected(self, Selection):
        if(Selection == "Modified Version 1 : Newton-Raphson"):
            self.m.setVisible(True)
        else:
            self.m.setVisible(False)
    
    try:
      def start(self):
        start_time=0
        end_time=0
        self.equation = self.equation_input.text()
        if(self.method_combo.currentText() == "Bisection"):
            start_time = time.perf_counter()
            self.result = Bisection(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
            end_time = time.perf_counter()
        elif(self.method_combo.currentText() == "False Position"):
            start_time = time.perf_counter()
            self.result = false_position(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
            end_time = time.perf_counter() 
        elif(self.method_combo.currentText() == "Fixed-Point Iteration"):
            start_time = time.perf_counter()
            self.result = FixedPoint(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text())) 
            end_time = time.perf_counter()
        elif(self.method_combo.currentText() == "Newton-Raphson Methods"):
            if(self.NR_method_combo.currentText() == "Original Newton-Raphson"):
                start_time = time.perf_counter()
                self.result = Original_Newton_Raphson(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
                end_time = time.perf_counter()
                self.sub_selection = "Secant"
            elif(self.NR_method_combo.currentText() == "Modified Version 1 : Newton-Raphson"):
                start_time = time.perf_counter()
                self.result = Modified1_Newton_Raphson(self.equation, float(self.initial_value_0.text()), self.significant_figures , int(self.m.text()) , float(self.Error_input.text()), float(self.Max_input.text()))
                end_time = time.perf_counter()
                self.sub_selection = "Secant"
            elif(self.NR_method_combo.currentText() == "Modified Version 2 : Newton-Raphson"):
                start_time = time.perf_counter()
                self.result = Modified2_Newton_Raphson(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
                end_time = time.perf_counter()
                self.sub_selection = "Modified Version 2 : Newton-Raphson"
        elif(self.method_combo.currentText() == "Secant Methods"):
            if(self.SE_method_combo.currentText() == "Secant Method"):
                start_time = time.perf_counter()
                self.result = Secant(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
                end_time = time.perf_counter()
            elif(self.SE_method_combo.currentText() == "Modified Secant Method"):
                start_time = time.perf_counter()
                self.result = ModifiedSecant(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
                end_time = time.perf_counter()
        self.results_label.setText(f"answer : {self.result.get('root')}\n"
        f"n iterations : {self.result.get('iterations')}\n"
        f"relative error : {self.result.get('relative_error')}\n"
        f"correct significant figures : {self.result.get('correct_Significant_Figures')}\n"
        f"function value : {self.result.get('function_value')}")
        for i in range(0,len(self.result.get('iteration_history'))):
            if(i < len(self.result.get('iteration_history')) - 1):
                self.results_history.addItem(f"Iteration {i + 1}")
            else:
                self.results_history.addItem("Final Iteration")
        self.results_history.setCurrentText("Final Iteration")
        self.results_label.setVisible(True)
        self.time = (end_time - start_time)*1000
        self.results_time.setText(f"Time : {self.time} ms")
        self.stacked_widget.setCurrentWidget(self.results_page)
    except Exception as e:
      ErrorHandler.show_error(e)
    def on_clear_back_button_click(self):
        self.show_input_page()
        self.clear_inputs()
    def return_back(self):
        self.show_input_page()
        self.get_last_update()
    def end(self):
        QApplication.quit()
    def show_input_page(self):
        self.stacked_widget.setCurrentWidget(self.input_page)
    def clear_inputs(self):
        self.equation_input.clear()
        self.initial_value_0.clear()
        self.initial_value_1.clear()
        self.initial_value_1.setVisible(True)
        self.Error_input.clear()
        self.Max_input.clear()
        self.equation = ""
        self.NR_method_combo.setVisible(False)
        self.SE_method_combo.setVisible(False)
        self.method_combo.setCurrentIndex(0)
        self.NR_method_combo.setCurrentIndex(0)
        self.SE_method_combo.setCurrentIndex(0)
        self.picked = "Bisection"
        self.sub_selection = "Secant"
    def get_last_update(self):
        self.equation = ""
        self.results_history.clear()

    def open_linear_window(self):
        self.open_equation_solver.emit()
        self.close()
    
    def open_main_window(self):
        self.return_to_main.emit()
        self.close()

    def change_result(self):
        index = self.results_history.currentIndex()
        print(f"Current Index: {index}\n")  # Debugging line
        print(f"Results History Count: {self.results_history.count()}\n")
        print(f"{self.picked}  {self.sub_selection}\n")
        if(index == self.results_history.count() - 1):
            self.results_label.setText(f"answer : {self.result.get('root')}\n"
            f"n iterations : {self.result.get('iterations')}\n"
            f"relative error : {self.result.get('relative_error')}\n"
            f"correct significant figures : {self.result.get('correct_Significant_Figures')}\n"
            f"function value : {self.result.get('function_value')}")
        else:
            if(self.picked == 'Bisection'):
                self.results_label.setText(f"xl: {self.result.get('iteration_history')[index].get('xl')}\n"
                                       f"xu: {self.result.get('iteration_history')[index].get('xu')}\n"
                                       f"xr: {self.result.get('iteration_history')[index].get('xr')}\n"
                                       f"f(xr): {self.result.get('iteration_history')[index].get('f(xr)')}\n"
                                       f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n"
                                       f"iteration: {self.result.get('iteration_history')[index].get('iteration')}")
            elif(self.picked == 'False Position'):
                self.results_label.setText(f"xl: {self.result.get('iteration_history')[index].get('xl')}\n"
                                       f"xu: {self.result.get('iteration_history')[index].get('xu')}\n"
                                       f"xr: {self.result.get('iteration_history')[index].get('xr')}\n"
                                       f"f(xr): {self.result.get('iteration_history')[index].get('f(xr)')}\n"
                                       f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n"
                                       f"iteration: {self.result.get('iteration_history')[index].get('iteration')}")  
            elif(self.picked == 'Fixed-Point Iteration'):
                self.results_label.setText(f"x_old: {self.result.get('iteration_history')[index].get('x_old')}\n"
                                       f"x_new: {self.result.get('iteration_history')[index].get('x_new')}\n"
                                       f"fx: {self.result.get('iteration_history')[index].get('fx')}\n"
                                       f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n"
                                       f"iteration: {self.result.get('iteration_history')[index].get('iteration')}")
            elif(self.picked == 'Newton-Raphson Methods'):
                self.results_label.setText(f"x: {self.result.get('iteration_history')[index].get('x')}\n"
                                       f"f(x): {self.result.get('iteration_history')[index].get('f(x)')}\n"
                                       f"f\'(x): {self.result.get('iteration_history')[index].get('f\'(x)')}\n"
                                        f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n")
                if(self.sub_selection == "Modified Version 2 : Newton-Raphson"):
                    self.results_label.setText(f"x: {self.result.get('iteration_history')[index].get('x')}\n"
                                       f"f(x): {self.result.get('iteration_history')[index].get('f(x)')}\n"
                                       f"f\'(x): {self.result.get('iteration_history')[index].get('f\'(x)')}\n"
                                        f"f\'\'(x): {self.result.get('iteration_history')[index].get('f\'\'(x)')}\n"
                                        f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n")
            elif(self.picked == 'Secant Methods'):
                if(self.sub_selection == 'Secant'):
                    self.results_label.setText(f"x0: {self.result.get('iteration_history')[index].get('x0')}\n"
                                       f"x1: {self.result.get('iteration_history')[index].get('x1')}\n"
                                       f"x2: {self.result.get('iteration_history')[index].get('x2')}\n"
                                       f"f(x0): {self.result.get('iteration_history')[index].get('fx0')}\n"
                                        f"f(x1): {self.result.get('iteration_history')[index].get('fx1')}\n"
                                       f"f(x2): {self.result.get('iteration_history')[index].get('fx2')}\n"
                                       f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n"
                                       f"iteration: {self.result.get('iteration_history')[index].get('iteration')}")
                elif(self.sub_selection == 'Modified Secant'):
                    self.results_label.setText(f"x: {self.result.get('iteration_history')[index].get('x')}\n"
                                               f"x_plus_delta: {self.result.get('iteration_history')[index].get('x_plus_delta')}\n"
                                               f"x_new: {self.result.get('iteration_history')[index].get('x_new')}\n"
                                               f"f(x): {self.result.get('iteration_history')[index].get('fx')}\n"
                                               f"f(x_plus_delta): {self.result.get('iteration_history')[index].get('fx_plus_delta')}\n"
                                                f"relative error: {self.result.get('iteration_history')[index].get('relative_error')}\n")
