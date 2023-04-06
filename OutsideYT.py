import sys
import os

from outside.oyt_gui import Ui_YouTubeOutside
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory, QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


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
        table = globals()[f'{current_page}_table']
        rows = table.rowCount()
        [table.setItem(i, 0, QTableWidgetItem(f"e{i + 1}")) for i in range(rows)]
        table.update()

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
    Upload_table = ui.Upload_Table
    Upload_table.verticalHeader().setSectionsMovable(True)
    ui.Upload_Progress_Bar.setVisible(False)

    Upload_table.setColumnCount(15)
    Upload_table.setHorizontalHeaderLabels(["id", "User", "Title", "Publ time", "Video", "Description",
                                            "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
                                            "Save title?", "Delete", "Select"])

    ui.Upload_SelectAll_CheckBox.stateChanged.connect(Upload.checkbox_changed)

    Upload_table.setDragEnabled(True)
    Upload_table.setDropIndicatorShown(True)
    Upload_table.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)


class Upload:

    @classmethod
    def checkbox_changed(cls, state):
        for i in range(Upload_table.rowCount()):
            if state == Qt.Checked:
                Upload_table.item(i, 14).setFlags(Upload_table.item(i, 14).flags() | Qt.ItemIsEnabled)
            else:
                Upload_table.item(i, 14).setFlags(Upload_table.item(i, 14).flags() & ~Qt.ItemIsEnabled)
        Upload_table.update()

    id = 1

    @classmethod
    def add_row_update_table(cls, user=None, video="-def", preview="-def",
                             title="-def", description="-def", playlist="-def",
                             tags="-def", ends="random", cards=1, publ_time=None,
                             access=0, save_title=False):
        row = Upload_table.rowCount()
        Upload_table.insertRow(row)
        Upload_table.setVerticalHeaderItem(row, QTableWidgetItem(">"))
        Upload_table.setItem(row, 0, QTableWidgetItem(f"{cls.id}"))
        Upload_table.setItem(row, 1, QTableWidgetItem("user"))
        Upload_table.setItem(row, 2, QTableWidgetItem(title))
        Upload_table.setItem(row, 3, QTableWidgetItem(publ_time))
        Upload_table.setItem(row, 4, QTableWidgetItem(video))
        Upload_table.setItem(row, 5, QTableWidgetItem(description))
        Upload_table.setItem(row, 6, QTableWidgetItem(playlist))
        Upload_table.setItem(row, 7, QTableWidgetItem(preview))
        Upload_table.setItem(row, 8, QTableWidgetItem(tags))
        Upload_table.setItem(row, 9, QTableWidgetItem(ends))
        Upload_table.setItem(row, 10, QTableWidgetItem(cards))
        Upload_table.setItem(row, 11, QTableWidgetItem(access))
        svt = QTableWidgetItem()
        svt.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if save_title:
            svt.setCheckState(Qt.Checked)
        else:
            svt.setCheckState(Qt.Unchecked)
        Upload_table.setItem(row, 12, svt)
        Upload_table.setItem(row, 13, QTableWidgetItem("Delete?"))
        chk = QTableWidgetItem()
        chk.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        chk.setCheckState(Qt.Checked)
        Upload_table.setItem(row, 14, chk)
        cls.id += 1
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
