from typing import Dict, Any

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QStyleFactory, QPushButton


def error_func(text, parent=None):
    error_dialog = QMessageBox(parent) if parent else QMessageBox()
    error_dialog = _set_box_style(error_dialog, title='Error', text=text)
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.exec_()


def warning_func(text, parent=None):
    warning_dialog = QMessageBox(parent) if parent else QMessageBox()
    warning_dialog = _set_box_style(warning_dialog, title='Warning', text=text)
    warning_dialog.setIcon(QtWidgets.QMessageBox.Question)

    yes_button = warning_dialog.addButton('Yes', QMessageBox.YesRole)
    warning_dialog.addButton('No', QMessageBox.NoRole)
    warning_dialog.exec_()
    if warning_dialog.clickedButton() == yes_button:
        return True
    return False


def waiting_func(text: str, time: int):
    waiting_dialog = QMessageBox()
    waiting_dialog = _set_box_style(waiting_dialog, title='Confirmation', text=f'{text}\n{time}')
    waiting_dialog.setIcon(QtWidgets.QMessageBox.Question)
    waiting_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    waiting_dialog.setDefaultButton(QMessageBox.No)
    waiting_dialog.setWindowModality(Qt.ApplicationModal)

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


def choose_func(text: str, vars: Dict, standart_var: Any):
    def close(event):
        choose_dialog.close()
        return -1
    choose_dialog = QMessageBox()
    choose_dialog = _set_box_style(choose_dialog, title='Choose option', text=text)
    for button_text, button_val in vars.items():
        new_button = QPushButton(button_text)
        if button_text == standart_var:
            new_button.setDefault(True)
        new_button.clicked.connect(lambda: choose_dialog.done(button_val))
        choose_dialog.addButton(new_button, QMessageBox.ActionRole)
        choose_dialog.closeEvent = close
    return choose_dialog.exec_()

def info_func(text: str):
    info_dialog = QMessageBox()
    info_dialog = _set_box_style(info_dialog, title='Information', text=text)
    info_dialog.setIcon(QtWidgets.QMessageBox.Information)
    info_dialog.exec_()

def _set_box_style(dialog, title: str, text: str = '',):
    dialog.setStyleSheet("""
        background-color: rgb(39, 39, 39);
        color: rgb(255, 255, 255);
        alternate-background-color: rgb(39, 39, 39);
        selection-background-color: rgb(15, 15, 15);
    """)
    dialog.setStyle(QStyleFactory.create('Fusion'))
    dialog.setText(text)
    dialog.setWindowTitle(title)
    return dialog
