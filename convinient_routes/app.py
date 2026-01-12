from PyQt6.QtWidgets import QWidget, QApplication
from main_page import MainPage

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    Form.show()
    ui = MainPage()
    ui.setupUi(Form)
    sys.exit(app.exec())
