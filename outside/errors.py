from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory


def error_func(text):
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText(text)
    error_dialog.setStyle(QStyleFactory.create("Fusion"))
    error_dialog.setWindowTitle("Error")
    error_dialog.exec_()