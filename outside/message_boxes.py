from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QStyleFactory


def error_func(text, parent=None):
    error_dialog = QMessageBox(parent) if parent else QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText(text)
    error_dialog.setStyle(QStyleFactory.create('Fusion'))
    error_dialog.setWindowTitle('Error')
    error_dialog.setStyleSheet("""
        background-color: rgb(39, 39, 39);
        color: rgb(255, 255, 255);
        alternate-background-color: rgb(39, 39, 39);
        selection-background-color: rgb(15, 15, 15);
    """)

    error_dialog.exec_()


def warning_func(text, parent=None):
    warning_dialog = QMessageBox(parent) if parent else QMessageBox()
    warning_dialog.setIcon(QtWidgets.QMessageBox.Question)
    warning_dialog.setText(text)
    warning_dialog.setStyle(QStyleFactory.create('Fusion'))
    warning_dialog.setWindowTitle('Warning')
    warning_dialog.setStyleSheet("""
        background-color: rgb(39, 39, 39);
        color: rgb(255, 255, 255);
        alternate-background-color: rgb(39, 39, 39);
        selection-background-color: rgb(15, 15, 15);
    """)

    yes_button = warning_dialog.addButton('Yes', QMessageBox.YesRole)
    warning_dialog.addButton('No', QMessageBox.NoRole)
    warning_dialog.exec_()
    if warning_dialog.clickedButton() == yes_button:
        return True
    return False


def waiting_func(text: str, time: int):
    waiting_dialog = QMessageBox()
    waiting_dialog.setIcon(QtWidgets.QMessageBox.Question)
    waiting_dialog.setStyle(QStyleFactory.create('Fusion'))
    waiting_dialog.setWindowTitle('Confirmation')
    waiting_dialog.setText(f'{text}\n{time}')
    waiting_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    waiting_dialog.setDefaultButton(QMessageBox.No)
    waiting_dialog.setWindowModality(Qt.ApplicationModal)
    waiting_dialog.setStyleSheet("""
        background-color: rgb(39, 39, 39);
        color: rgb(255, 255, 255);
        alternate-background-color: rgb(39, 39, 39);
        selection-background-color: rgb(15, 15, 15);
    """)

    def updateCountdown():
        seconds_left = int(waiting_dialog.text().split('\n')[-1])
        if seconds_left > 0:
            seconds_left -= 1
            waiting_dialog.setText(f'{text}\n{seconds_left}')
        else:
            timer.stop()
            waiting_dialog.accept()

    timer = QtCore.QTimer()
    timer.timeout.connect(updateCountdown)
    timer.start(time * 500)
    result = waiting_dialog.exec_()
    if result in [QMessageBox.Accepted, QMessageBox.Yes]:
        return True
    return False
