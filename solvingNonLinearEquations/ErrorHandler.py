from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
import sys
import traceback

class ErrorHandler:
    @staticmethod
    def show_error(message, details=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        if details:
            msg.setDetailedText(details)
        msg.setStyleSheet("""
        QMessageBox {
            background-color: #2b2b2b;  /* Dark background */
            color: #f8f8f2;  /* Light text */
            font-family: Arial, sans-serif; /* Font family */
            font-size: 14px; /* Text size */
        }
        QMessageBox QPushButton {
            background-color: #5c6370;  /* Button background */
            color: #ffffff;  /* Button text color */
            border: 1px solid #4b5263;  /* Button border */
            padding: 5px 15px;
            border-radius: 5px;  /* Rounded corners */
        }
        QMessageBox QPushButton:hover {
            background-color: #3e4451;  /* Hover background */
        }
        QMessageBox QLabel {
            color: #f8f8f2;  /* Label text color */
            font-size: 14px; /* Label text size */
        }
    """)
        msg.exec_()

def exception_hook(exctype, value, traceback_obj):
    """Global exception handler for unhandled exceptions"""
    error_msg = '\n'.join([''.join(traceback.format_tb(traceback_obj)),
                          f'{exctype.__name__}: {value}'])
    ErrorHandler.show_error("An unexpected error occurred", error_msg)

# Set global exception handler
sys.excepthook = exception_hook