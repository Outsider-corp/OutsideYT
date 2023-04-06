import functools
import sys
import os

from oyt_gui import Ui_YouTubeOutside
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory, QMainWindow, QShortcut, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


class QMainWindowPlus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shortcut = QShortcut(QKeySequence('F5'), self)
        self.shortcut.activated.connect(QMainWindowPlus.table_update)

        self.shortcut = QShortcut(QKeySequence('Ctrl+Shift+E'), self)
        self.shortcut.activated.connect(QMainWindowPlus.open_main_folder)

        self.shortcut = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcut.activated.connect(QMainWindowPlus.add_row)

    @classmethod
    def open_main_folder(cls):
        os.startfile(os.getcwd())

    @classmethod
    def table_update(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        # globals()[f'{current_page}_table'] = globals()[f'add_row_{current_page.lower()}_table']()
        # globals()[f'{current_page}_table'].show()

    @classmethod
    def add_row(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        table = globals()[f'{current_page}_table']
        table = Upload.add_row_update_table(table)
        table.show()


def update_ui():
    update_upload()
    update_watch()
    update_download()


def update_upload():
    global Upload_table

    ui.Upload_Progress_Bar.setVisible(False)

    Upload_table = ui.Upload_Table
    Upload_table.setColumnCount(14)
    Upload_table.setHorizontalHeaderLabels(["User", "Title", "Publ time", "Video", "Description",
                                            "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
                                            "Save title?", "Delete", "Select"])

    ui.Upload_SelectAll_CheckBox.stateChanged.connect(Upload.checkbox_changed)


class Upload:

    @classmethod
    def checkbox_changed(cls, state):
        for i in range(Upload_table.rowCount()):
            if state == Qt.Checked:
                Upload_table.item(i, 13).setFlags(Upload_table.item(i, 13).flags() | Qt.ItemIsEnabled)
            else:
                Upload_table.item(i, 13).setFlags(Upload_table.item(i, 13).flags() & ~Qt.ItemIsEnabled)
        Upload_table.update()

    @classmethod
    def add_row_update_table(cls, user=None, video="-def", preview="-def",
                             title="-def", description="-def", playlist="-def",
                             tags="-def", ends="random", cards=1, publ_time=None,
                             access=0, save_title=False):
        table = Upload_table
        row = table.rowCount()
        Upload_table.insertRow(row)
        Upload_table.setItem(row, 0, QTableWidgetItem("user"))
        Upload_table.setItem(row, 1, QTableWidgetItem(title))
        Upload_table.setItem(row, 2, QTableWidgetItem(publ_time))
        Upload_table.setItem(row, 3, QTableWidgetItem(video))
        Upload_table.setItem(row, 4, QTableWidgetItem(description))
        Upload_table.setItem(row, 5, QTableWidgetItem(playlist))
        Upload_table.setItem(row, 6, QTableWidgetItem(preview))
        Upload_table.setItem(row, 7, QTableWidgetItem(tags))
        Upload_table.setItem(row, 8, QTableWidgetItem(ends))
        Upload_table.setItem(row, 9, QTableWidgetItem(cards))
        Upload_table.setItem(row, 10, QTableWidgetItem(access))
        svt = QTableWidgetItem()
        svt.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if save_title:
            svt.setCheckState(Qt.Checked)
        else:
            svt.setCheckState(Qt.Unchecked)
        Upload_table.setItem(row, 11, svt)
        Upload_table.setItem(row, 12, QTableWidgetItem("Delete?"))
        chk = QTableWidgetItem()
        chk.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chk.setCheckState(Qt.Checked)
        Upload_table.setItem(row, 13, chk)
        return Upload_table


def update_watch():
    global Watch_table

    ui.Watch_Progress_Bar.setVisible(False)

    Watch_table = ui.Watch_Table
    Watch_table.setColumnCount(5)
    Watch_table.setHorizontalHeaderLabels(["Watchers Group", "Video", "Channel", "Delete", "Select"])


def update_download():
    global Download_table

    ui.Download_SavingPath_Label.setText("videos/")
    ui.Download_Progress_Bar.setVisible(False)

    Download_table = ui.Download_Table
    Download_table.setColumnCount(5)
    Download_table.setHorizontalHeaderLabels(["Channel", "Video", "Folder", "Delete", "Select"])


def start_GUI():
    global app, YouTubeOutside, ui, Upload_table, Download_table, Watch_table
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    YouTubeOutside = QMainWindowPlus()
    ui = Ui_YouTubeOutside()
    ui.setupUi(YouTubeOutside)
    update_ui()
    YouTubeOutside.show()


if __name__ == '__main__':
    start_GUI()

    sys.exit(app.exec_())
