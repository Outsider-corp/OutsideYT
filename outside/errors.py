from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory, QMessageBox


def error_func(text):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText(text)
    error_dialog.setStyle(QStyleFactory.create("Fusion"))
    error_dialog.setWindowTitle("Error")
    error_dialog.exec_()

def warning_func(text):
    dialog = QMessageBox()
    dialog.setIcon(QtWidgets.QMessageBox.Question)
    dialog.setText(text)
    dialog.setStyle(QStyleFactory.create("Fusion"))
    dialog.setWindowTitle("Warning")
    yes_button = dialog.addButton("Yes", QMessageBox.YesRole)
    no_button = dialog.addButton("No", QMessageBox.NoRole)
    dialog.exec_()
    if dialog.clickedButton() == yes_button:
        return True
    return False
