from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextBrowser, QCheckBox, QMainWindow, QDateEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QDate
import sys
import os
from Convinient_routes.convinient_routes import calculate_route

current_dir = os.path.dirname(__file__)


class MainPage(QMainWindow):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 800)
        Form.setStyleSheet("""
            background-color: #87ceeb;
            font-family: 'Arial';
        """)

        self.main_layout = QVBoxLayout(Form)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(20)

        # Заголовок
        self.header_label = QLabel("Поиск маршрутов")
        self.header_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: #1a237e;
            margin-bottom: 20px;
        """)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.header_label)

        # Чекбоксы для выбора транспорта
        self.setupTransportCheckboxes()
        self.main_layout.addLayout(self.checkbox_layout)

        # Верхняя строка - города
        self.cities_layout = QHBoxLayout()
        self.setupCitiesInput()
        self.main_layout.addLayout(self.cities_layout)

        # Нижняя строка - даты и кнопка поиска
        self.dates_layout = QHBoxLayout()
        self.setupDatesInput()
        self.main_layout.addLayout(self.dates_layout)

        # Область вывода результатов
        self.results_layout = QHBoxLayout()
        self.setupResultsDisplay()
        self.main_layout.addLayout(self.results_layout)

        self.retranslateUi(Form)

    def setupTransportCheckboxes(self):
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.setSpacing(30)
        self.checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icons = {
            "bus": {
                "color": os.path.join(current_dir, "icons", "bus.png"),
                "gray": os.path.join(current_dir, "icons", "grey bus.png")
            },
            "train": {
                "color": os.path.join(current_dir, "icons", "train.png"),
                "gray": os.path.join(current_dir, "icons", "grey train.png")
            },
            "plane": {
                "color": os.path.join(current_dir, "icons", "plane.png"),
                "gray": os.path.join(current_dir, "icons", "grey plane.png")
            }
        }

        self.checkBox_bus = QCheckBox()
        self.checkBox_bus.setIcon(QIcon(self.icons["bus"]["color"]))
        self.checkBox_bus.setIconSize(QtCore.QSize(80, 80))
        self.checkBox_bus.setStyleSheet(self.getCheckboxStyle())
        self.checkBox_bus.stateChanged.connect(lambda: self.toggle_icon(self.checkBox_bus, "bus"))

        self.checkBox_train = QCheckBox()
        self.checkBox_train.setIcon(QIcon(self.icons["train"]["color"]))
        self.checkBox_train.setIconSize(QtCore.QSize(80, 80))
        self.checkBox_train.setStyleSheet(self.getCheckboxStyle())
        self.checkBox_train.stateChanged.connect(lambda: self.toggle_icon(self.checkBox_train, "train"))

        self.checkBox_plane = QCheckBox()
        self.checkBox_plane.setIcon(QIcon(self.icons["plane"]["color"]))
        self.checkBox_plane.setIconSize(QtCore.QSize(80, 80))
        self.checkBox_plane.setStyleSheet(self.getCheckboxStyle())
        self.checkBox_plane.stateChanged.connect(lambda: self.toggle_icon(self.checkBox_plane, "plane"))

        self.checkbox_layout.addWidget(self.checkBox_bus)
        self.checkbox_layout.addWidget(self.checkBox_train)
        self.checkbox_layout.addWidget(self.checkBox_plane)

    def setupCitiesInput(self):
        # Город отправления
        self.lineEdit_departure = QLineEdit()
        self.lineEdit_departure.setPlaceholderText("Город отправления")
        self.lineEdit_departure.setStyleSheet(self.getInputStyle())
        self.cities_layout.addWidget(self.lineEdit_departure, stretch=2)

        self.icon = {
            "swap":
            {
                "color": os.path.join(current_dir, "icons", "free-icon-swap-318147.png")
            }
        }

        # Кнопка замены городов (белый фон)
        self.swap_button = QPushButton()
        self.swap_button.setIcon(QIcon(self.icon["swap"]["color"]))
        self.swap_button.setIconSize(QtCore.QSize(24, 24))
        self.swap_button.setStyleSheet("""
            QPushButton {
                background-color: #87ceeb;
                border: 1px solid #000000;
                border-radius: 4px;
                padding: 10px;
                min-width: 40px;
                max-width: 40px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        self.swap_button.setToolTip("Поменять местами города")
        self.swap_button.clicked.connect(self.swap_cities)
        self.cities_layout.addWidget(self.swap_button, stretch=0)

        # Город прибытия
        self.lineEdit_arrival = QLineEdit()
        self.lineEdit_arrival.setPlaceholderText("Город прибытия")
        self.lineEdit_arrival.setStyleSheet(self.getInputStyle())
        self.cities_layout.addWidget(self.lineEdit_arrival, stretch=2)

    def setupDatesInput(self):
        # Дата отправления (только дата, без времени)
        self.lineEdit_departure_time = QDateEdit()
        self.lineEdit_departure_time.setDisplayFormat("yyyy-MM-dd")
        self.lineEdit_departure_time.setDate(QDate.currentDate())
        self.lineEdit_departure_time.setCalendarPopup(True)
        self.lineEdit_departure_time.setStyleSheet("""
              QDateEdit {
                  padding: 8px;
                  font-size: 16px;
                  border: 1px solid #000000;
                  border-radius: 4px;
              }
              QDateEdit::drop-down {
                  subcontrol-origin: padding;
                  subcontrol-position: center right;
                  width: 24px;
                  border-left: 1px solid #000000;
                  image: url(%s);
              }
              QDateEdit::down-arrow {
                  image: none;
              }
              QDateEdit:focus {
                  border: 1px solid #2196F3;
              }
          """ % os.path.join(current_dir, "icons", "free-icon-calendar-5858931.png").replace("\\", "/"))

        self.dates_layout.addWidget(self.lineEdit_departure_time, stretch=1)

        # Дата прибытия (только дата, без времени)
        self.lineEdit_arrival_time = QDateEdit()
        self.lineEdit_arrival_time.setDisplayFormat("yyyy-MM-dd")
        self.lineEdit_arrival_time.setDate(QDate.currentDate().addDays(1))
        self.lineEdit_arrival_time.setCalendarPopup(True)
        self.lineEdit_arrival_time.setStyleSheet("""
              QDateEdit {
                  padding: 8px;
                  font-size: 16px;
                  border: 1px solid #000000;
                  border-radius: 4px;
              }
              QDateEdit::drop-down {
                  subcontrol-origin: padding;
                  subcontrol-position: center right;
                  width: 24px;
                  border-left: 1px solid #000000;
                  image: url(%s);
              }
              QDateEdit::down-arrow {
                  image: none;
              }
              QDateEdit:focus {
                  border: 1px solid #2196F3;
              }
          """ % os.path.join(current_dir, "icons", "free-icon-calendar-5858931.png").replace("\\", "/"))

        self.dates_layout.addWidget(self.lineEdit_arrival_time, stretch=1)

        # Кнопка поиска (остается без изменений)
        self.calculate_button = QPushButton("Найти маршруты")
        self.calculate_button.setStyleSheet("""
              QPushButton {
                  background-color: #ff6d00;
                  color: #ffffff;
                  border: 2px solid #000000;
                  border-radius: 4px;
                  padding: 12px 20px;
                  font-size: 16px;
                  font-weight: bold;
                  min-height: 40px;
              }
              QPushButton:hover {
                  background-color: #fff3e0;
              }
              QPushButton:pressed {
                  background-color: #ffe0b2;
              }
          """)
        self.calculate_button.clicked.connect(self.on_calculate_button_click)
        self.dates_layout.addWidget(self.calculate_button, stretch=1)

    def setupResultsDisplay(self):
        self.textBrowser_bus = QTextBrowser()
        self.textBrowser_bus.setStyleSheet(self.getResultStyle())
        self.results_layout.addWidget(self.textBrowser_bus)

        self.textBrowser_train = QTextBrowser()
        self.textBrowser_train.setStyleSheet(self.getResultStyle())
        self.results_layout.addWidget(self.textBrowser_train)

        self.textBrowser_plane = QTextBrowser()
        self.textBrowser_plane.setStyleSheet(self.getResultStyle())
        self.results_layout.addWidget(self.textBrowser_plane)

    def getCheckboxStyle(self):
        return """
            QCheckBox {
                spacing: 10px;
                font-size: 16px;
                color: #333;
            }
            QCheckBox::indicator {
                width: 0px;
                height: 0px;
            }
        """

    def getInputStyle(self):
        return """
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border: 1px solid #000000;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """

    def getDateStyle(self):
        return """
            QDateEdit {
                padding: 8px;
                font-size: 16px;
                border: 1px solid #000000;
                border-radius: 4px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border-left: 1px solid #000000;
            }
            QDateEdit:focus {
                border: 1px solid #2196F3;
            }
        """

    def getResultStyle(self):
        return """
            QTextBrowser {
                background-color: white;
                border: 1px solid #000000;;
                border-radius: 4px;
                padding: 15px;
                font-size: 14px;
            }
        """

    def toggle_icon(self, checkbox, transport_type):
        if checkbox.isChecked():
            checkbox.setIcon(QIcon(self.icons[transport_type]["gray"]))
        else:
            checkbox.setIcon(QIcon(self.icons[transport_type]["color"]))

    def format_date(self, qdate):
        """Преобразует QDate в строку формата ГГГГ-ММ-ДД"""
        return qdate.toString("yyyy-MM-dd")

    def swap_cities(self):
        departure = self.lineEdit_departure.text()
        arrival = self.lineEdit_arrival.text()
        self.lineEdit_departure.setText(arrival)
        self.lineEdit_arrival.setText(departure)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Поиск маршрутов"))

    def on_calculate_button_click(self):
        self.textBrowser_bus.clear()
        self.textBrowser_train.clear()
        self.textBrowser_plane.clear()

        departure_city = self.lineEdit_departure.text()
        arrival_city = self.lineEdit_arrival.text()

        # Получаем даты в нужном формате ГГГГ-ММ-ДД
        departure_date = self.format_date(self.lineEdit_departure_time.date())
        arrival_date = self.format_date(self.lineEdit_arrival_time.date())

        # Проверяем наличие введенных данных
        if not departure_city or not arrival_city:
            self.show_error("Введите города отправления и прибытия", "Ошибка ввода данных")
            return

        # Проверяем, что хотя бы один вид транспорта выбран
        if not (self.checkBox_bus.isChecked() or self.checkBox_train.isChecked() or self.checkBox_plane.isChecked()):
            self.show_error("Выберите хотя бы один вид транспорта", "Ошибка выбора транспорта")
            return

        # Получаем результаты (передаем даты без времени)
        results = calculate_route.process_cities(departure_city, arrival_city, departure_date, arrival_date)
        if results:
            for result in results:
                transport = result.get('type')
                from_city = result.get('from', 'Не указано')
                to_city = result.get('to', 'Не указано')
                departure = result.get('departure', 'Не указано')
                arrival = result.get('arrival', 'Не указано')
                travel_time = result.get('travel_time', 'Не указано')
                route_number = result.get('route_number', 'Не указано')

                if transport == 'plane':
                    insert_tr = "Самолёт"
                elif transport == "train":
                    insert_tr = "Поезд"
                else:
                    insert_tr = "Автобус"

                route_info = (
                    f"<b>Маршрут:</b><br>"
                    f"<b>Тип транспорта:</b> {insert_tr}<br>"
                    f"<b>Откуда:</b> {from_city}<br>"
                    f"<b>Куда:</b> {to_city}<br>"
                    f"<b>Дата отправления:</b> {departure}<br>"
                    f"<b>Дата прибытия:</b> {arrival}<br>"
                    f"<b>Время в пути:</b> {travel_time}<br>"
                )

                if route_number:
                    route_info += f"<b>Номер рейса:</b> {route_number}<br><br>"
                else:
                    route_info += "<br>"

                if transport == "bus" and self.checkBox_bus.isChecked():
                    self.textBrowser_bus.append(route_info)
                elif transport == "train" and self.checkBox_train.isChecked():
                    self.textBrowser_train.append(route_info)
                elif transport == "plane" and self.checkBox_plane.isChecked():
                    self.textBrowser_plane.append(route_info)

        # Очищаем текстовые браузеры, если соответствующие чекбоксы не установлены
        if not self.checkBox_bus.isChecked():
            self.textBrowser_bus.clear()
        if not self.checkBox_train.isChecked():
            self.textBrowser_train.clear()
        if not self.checkBox_plane.isChecked():
            self.textBrowser_plane.clear()

    def show_error(self, message, ErrCode):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle(ErrCode)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QMessageBox QLabel {
                color: #333;
            }
            QMessageBox QPushButton {
                background-color: #ff6d00;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #ff8500;
            }
        """)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = MainPage()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())