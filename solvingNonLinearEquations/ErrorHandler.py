from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
import sys
import traceback

class ErrorHandler:
    @staticmethod
    def show_error(message, details=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        if details:
            msg.setDetailedText(details)
        msg.exec_()

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.input = QLineEdit()
        self.result_label = QLabel()
        self.calc_button = QPushButton('Calculate')
        
        layout.addWidget(self.input)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)
        
        self.calc_button.clicked.connect(self.safe_calculate)

    def safe_calculate(self):
        try:
            # Example calculation that might raise errors
            expression = self.input.text()
            result = eval(expression)  # Note: eval is used for demonstration only
            self.result_label.setText(f"Result: {result}")
        except Exception as e:
            ErrorHandler.show_error(
                "Calculation Error",
                f"Error details:\n{str(e)}\n\n{traceback.format_exc()}"
            )

def exception_hook(exctype, value, traceback_obj):
    """Global exception handler for unhandled exceptions"""
    error_msg = '\n'.join([''.join(traceback.format_tb(traceback_obj)),
                          f'{exctype.__name__}: {value}'])
    ErrorHandler.show_error("An unexpected error occurred", error_msg)

# Set global exception handler
sys.excepthook = exception_hook