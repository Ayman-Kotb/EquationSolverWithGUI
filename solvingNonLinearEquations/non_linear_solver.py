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
import sys

class NonLinearSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.first = 0
        self.sec = 1 
        self.variables = 2  # Default number of variables
        self.significant_figures = 2  # Default significant figures
        self.equation = ""
        self.result = []
        self.sub_selection = ""

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

    def Change_Precision(self):
        self.significant_figures = self.sig_slider.value()
        self.sig_current.setText(f": {self.significant_figures}")

    def method_selected(self, Selection):
        if((Selection == "Bisection") | (Selection == "False Position")):
            self.initial_value_1.setVisible(True)
            self.NR_method_label.setVisible(False)
            self.SE_method_label.setVisible(False)
            self.SE_method_combo.setVisible(False)
            self.NR_method_combo.setVisible(False)
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
        else:
            self.initial_value_1.setVisible(False)
            self.NR_method_label.setVisible(False)
            self.SE_method_label.setVisible(False)
            self.SE_method_combo.setVisible(False)
            self.NR_method_combo.setVisible(False)

    def SE_method_selected(self, Selection):
        if(Selection == "Secant Method"):
            self.initial_value_1.setPlaceholderText("Enter the second initial value: ")
        else:
            self.initial_value_1.setPlaceholderText("Enter the delta value: ")
    def start(self):
        self.equation = self.equation_input.text()
        if(self.method_combo.currentText() == "Bisection"):
            self.result = Bisection(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
        elif(self.method_combo.currentText() == "False Position"):
            self.result = false_position(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
        elif(self.method_combo.currentText() == "Fixed-Point Iteration"):
            self.result = FixedPoint(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text())) 
        elif(self.method_combo.currentText() == "Newton-Raphson Methods"):
            if(self.NR_method_combo.currentText() == "Original Newton-Raphson"):
                self.result = Original_Newton_Raphson(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
            elif(self.NR_method_combo.currentText() == "Modified Version 1 : Newton-Raphson"):
                self.result = Modified1_Newton_Raphson(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
            elif(self.NR_method_combo.currentText() == "Modified Version 2 : Newton-Raphson"):
                self.result = Modified2_Newton_Raphson(self.equation, float(self.initial_value_0.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
        elif(self.method_combo.currentText() == "Secant Methods"):
            if(self.SE_method_combo.currentText() == "Secant Method"):
                self.result = Secant(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
            elif(self.SE_method_combo.currentText() == "Modified Secant Method"):
                self.result = ModifiedSecant(self.equation, float(self.initial_value_0.text()), float(self.initial_value_1.text()), self.significant_figures , float(self.Error_input.text()), float(self.Max_input.text()))
        
        self.results_label.setText(f"{self.result}")  # Add to the list
        self.results_label.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.results_page)

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
    def get_last_update(self):
        self.equation = ""
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = NonLinearSolver()
    main_window.show()
    sys.exit(app.exec_())
