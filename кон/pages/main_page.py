from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import modules.calculate_route
from PyQt6.QtWidgets import (
    QApplication, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser,
    QCheckBox, QMainWindow
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os

# Получаем путь к текущему файлу (main.py)
current_dir = os.path.dirname(__file__)

# Формируем путь к изображению
image_path = os.path.join(current_dir, "icons", "bus.png")

print(image_path)  # Проверяем путь
class main_page(QMainWindow):
    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(1000, 800)
        Form.setStyleSheet("background-color:rgb(173, 216, 230);")

        self.main_layout = QVBoxLayout(Form)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)

        # Поля ввода городов и времени
        self.input_layout = QHBoxLayout()

        self.departure_layout = QVBoxLayout()
        self.lineEdit_departure = QLineEdit()
        self.lineEdit_departure.setPlaceholderText("Город отправки")
        self.lineEdit_departure.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.departure_layout.addWidget(self.lineEdit_departure)

        self.lineEdit_departure_time = QLineEdit()
        self.lineEdit_departure_time.setPlaceholderText("Время отправления (YYYY-MM-DDTHH:MM:SS)")
        self.lineEdit_departure_time.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.departure_layout.addWidget(self.lineEdit_departure_time)

        self.input_layout.addLayout(self.departure_layout)

        self.arrival_layout = QVBoxLayout()
        self.lineEdit_arrival = QLineEdit()
        self.lineEdit_arrival.setPlaceholderText("Город прибытия")
        self.lineEdit_arrival.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.arrival_layout.addWidget(self.lineEdit_arrival)

        self.lineEdit_arrival_time = QLineEdit()
        self.lineEdit_arrival_time.setPlaceholderText("Время прибытия (YYYY-MM-DDTHH:MM:SS)")
        self.lineEdit_arrival_time.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.arrival_layout.addWidget(self.lineEdit_arrival_time)

        self.input_layout.addLayout(self.arrival_layout)

        self.main_layout.addLayout(self.input_layout)

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

        # Чекбоксы для выбора маршрута с иконками
        self.checkbox_layout = QHBoxLayout()

        # Создание чекбоксов с иконками
        self.checkBox_bus = QCheckBox()
        self.checkBox_bus.setIcon(QIcon(self.icons["bus"]["color"]))
        self.checkBox_bus.setIconSize(QtCore.QSize(100, 100))
        self.checkBox_bus.setStyleSheet("QCheckBox { padding: 0; } QCheckBox::indicator { width: 0px; height: 0px; }")
        self.checkBox_bus.stateChanged.connect(lambda: self.toggle_icon(self.checkBox_bus, "bus"))

        self.checkBox_train = QCheckBox()
        self.checkBox_train.setIcon(QIcon(self.icons["train"]["color"]))
        self.checkBox_train.setIconSize(QtCore.QSize(100, 100))
        self.checkBox_train.setStyleSheet("QCheckBox { padding: 0; } QCheckBox::indicator { width: 0px; height: 0px; }")
        self.checkBox_train.stateChanged.connect(lambda: self.toggle_icon(self.checkBox_train, "train"))

        self.checkBox_plane = QCheckBox()
        self.checkBox_plane.setIcon(QIcon(self.icons["plane"]["color"]))
        self.checkBox_plane.setIconSize(QtCore.QSize(100, 100))
        self.checkBox_plane.setStyleSheet("QCheckBox { padding: 0; } QCheckBox::indicator { width: 0px; height: 0px; }")
        self.checkBox_plane.stateChanged.connect(lambda: self.toggle_icon(self.checkBox_plane, "plane"))

        self.checkbox_layout.addWidget(self.checkBox_bus)
        self.checkbox_layout.addWidget(self.checkBox_train)
        self.checkbox_layout.addWidget(self.checkBox_plane)

        self.main_layout.addLayout(self.checkbox_layout)

        self.pushButton = QPushButton("Рассчитать маршрут")
        self.pushButton.setStyleSheet(
            "border-radius:10px; background-color: rgb(218, 200, 32); border:1px solid rgb(0, 0, 0);"
        )
        self.main_layout.addWidget(self.pushButton)

        # Область вывода результатов (горизонтальная ориентация)
        self.text_browser_layout = QHBoxLayout()

        self.textBrowser_bus = QTextBrowser()
        self.textBrowser_bus.setStyleSheet(
            "border-radius:10px; background-color: rgb(255, 255, 255);")
        self.text_browser_layout.addWidget(self.textBrowser_bus)

        self.textBrowser_train = QTextBrowser()
        self.textBrowser_train.setStyleSheet(
            "border-radius:10px; background-color: rgb(255, 255, 255);")
        self.text_browser_layout.addWidget(self.textBrowser_train)

        self.textBrowser_plane = QTextBrowser()
        self.textBrowser_plane.setStyleSheet(
            "border-radius:10px; background-color: rgb(255, 255, 255);")
        self.text_browser_layout.addWidget(self.textBrowser_plane)

        self.main_layout.addLayout(self.text_browser_layout)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.on_calculate_button_click)
    def toggle_icon(self, checkbox, transport_type):
        """Меняет иконку чекбокса при нажатии."""
        if checkbox.isChecked():
            checkbox.setIcon(QIcon(self.icons[transport_type]["gray"]))
        else:
            checkbox.setIcon(QIcon(self.icons[transport_type]["color"]))
        # Кнопка для расчета маршрута


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Маршруты"))

    def on_calculate_button_click(self):
        self.textBrowser_bus.clear()
        self.textBrowser_train.clear()
        self.textBrowser_plane.clear()
        departure_city = self.lineEdit_departure.text()
        arrival_city = self.lineEdit_arrival.text()
        departure_time = self.lineEdit_departure_time.text()
        arrival_time = self.lineEdit_arrival_time.text()

        # Проверяем наличие введенных данных
        if not departure_city or not arrival_city or not departure_time or not arrival_time:
            self.show_error("Введите все обязательные поля.",
                            "Ошибка ввода данных")
            return

        # Проверяем, что хотя бы один вид транспорта выбран
        if not (
                self.checkBox_bus.isChecked() or self.checkBox_train.isChecked() or self.checkBox_plane.isChecked()):
            self.show_error("Выберите хотя-бы один вид транспорта",
                            "Ошибка выбора транспорта")
            return

        # Получаем результаты
        results = modules.calculate_route.process_cities(departure_city, arrival_city, departure_time, arrival_time)
        if results:
            for result in results:
                transport = result.get('type')
                from_city = result.get('from', 'Не указано')
                to_city = result.get('to', 'Не указано')
                departure = result.get('departure', 'Не указано')
                arrival = result.get('arrival', 'Не указано')
                travel_time = result.get('travel_time', 'Не указано')
                route_number = result.get('route_number', 'Не указано')

                # Формируем текст для вывода
                route_info = (
                    f"Маршрут:\nТип транспорта: {transport}\n"
                    f"Откуда: {from_city}, Куда: {to_city}\n"
                    f"Время отправления: {departure}, Время прибытия: {arrival}\n"
                    f"Время в пути: {travel_time}\nНомер рейса: {route_number}\n\n"
                )

                # Выводим результаты в зависимости от выбранных чекбоксов
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
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
