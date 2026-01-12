from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from time import sleep
from pages.main_page import main_page

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    Form.show()
    ui = main_page()
    ui.setupUi(Form)
    sys.exit(app.exec())
