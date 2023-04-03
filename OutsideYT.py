import sys
import os

from oyt_gui import Ui_YouTubeOutside
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory, QMainWindow, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


class QMainWindowPlus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shortcut = QShortcut(QKeySequence('F5'), self)
        self.shortcut.activated.connect(update_form)

        self.shortcut = QShortcut(QKeySequence('Ctrl+Shift+E'), self)
        self.shortcut.activated.connect(open_main_folder)


def update_form():
    current_page = ui.OutsideYT.currentIndex()
    print(current_page)
    if current_page == 0:
        if ui.Upload_Progress_Label.text() == '':
            ui.Upload_Progress_Label.setText("Вы нажали F5, да?")
        else:
            ui.Upload_Progress_Label.setText('')
    elif current_page == 1:
        if ui.Watch_Progress_Label.text() == '':
            ui.Watch_Progress_Label.setText("Вы нажали F5, да?")
        else:
            ui.Watch_Progress_Label.setText('')
    elif current_page == 2:
        if ui.Download_Progress_Label.text() == ' ':
            ui.Download_Progress_Label.setText("Вы нажали F5, да?")
        else:
            ui.Download_Progress_Label.setText('')


def open_main_folder():
    os.startfile(os.getcwd())


def start_GUI():
    global app, YouTubeOutside, ui
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    YouTubeOutside = QMainWindowPlus()
    ui = Ui_YouTubeOutside()
    ui.setupUi(YouTubeOutside)
    YouTubeOutside.show()
    ui.Download_SavingPath_Label.setText("videos/")
    ui.Upload_Progress_Bar.setVisible(False)
    ui.Watch_Progress_Bar.setVisible(False)
    ui.Download_Progress_Bar.setVisible(False)

def table_update(page):
    table = getattr(ui, f'{page}_Table')

    table1 = ui.Upload_Table.


if __name__ == '__main__':
    start_GUI()

    sys.exit(app.exec_())
