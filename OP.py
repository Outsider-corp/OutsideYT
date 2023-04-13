import sys
import os

import pandas as pd

import OutsideYT
from outside.oyt_gui import Ui_YouTubeOutside
from outside.oyt_info import settings
from outside import TableModels, YT_Uploader

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QStyleFactory, QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class QMainWindowPlus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shortcut1 = QShortcut(QKeySequence('F5'), self)
        self.shortcut1.activated.connect(QMainWindowPlus.table_update)

        self.shortcut2 = QShortcut(QKeySequence('Ctrl+Shift+E'), self)
        self.shortcut2.activated.connect(QMainWindowPlus.open_main_folder)

        self.shortcut3 = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcut3.activated.connect(QMainWindowPlus.add_row)

        self.shortcut4 = QShortcut(QKeySequence('Ctrl+R'), self)
        self.shortcut4.activated.connect(QMainWindowPlus.login_google)

    @classmethod
    def open_main_folder(cls):
        os.startfile(os.getcwd())

    @classmethod
    def table_update(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        table = globals()[f'temp_table']
        print(table.model().get_data().iloc[0])
        table.update()

    @classmethod
    def add_row(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        table = globals()[f'{current_page}_table']
        if current_page == "Upload":
            table = Upload.add_row_update_table(table)
        elif current_page == "temp":
            table.model().insertRows()
        table.update()

    @classmethod
    def login_google(cls):
        table = globals()['temp_table']
        login = table.model().get_data().loc[0, "Title"]
        mail = table.model().get_data().loc[0, "Description"]
        YT_Uploader.google_login(login, mail)


def update_ui():
    global temp_table
    temp_table = ui.test_view
    Upload_model = TableModels.UploadModel()
    temp_table.setModel(Upload_model)
    update_upload()
    update_watch()
    update_download()
    update_upload_new()


def update_upload_new():
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    temp_table.setFont(font)
    temp_table.setFrameShape(QtWidgets.QFrame.StyledPanel)
    temp_table.setFrameShadow(QtWidgets.QFrame.Sunken)
    temp_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
    temp_table.setAlternatingRowColors(False)
    temp_table.setTextElideMode(Qt.ElideRight)
    temp_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    temp_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    temp_table.setGridStyle(Qt.SolidLine)
    temp_table.horizontalHeader().setCascadingSectionResizes(False)
    temp_table.horizontalHeader().setStretchLastSection(False)

    temp_table.setVerticalHeader(TableModels.HeaderView(temp_table))

    temp_table.verticalHeader().setCascadingSectionResizes(False)
    temp_table.verticalHeader().setStretchLastSection(False)
    temp_table.verticalHeader().setSectionsMovable(True)
    temp_table.setDragEnabled(True)
    temp_table.setDropIndicatorShown(True)
    temp_table.setDefaultDropAction(QtCore.Qt.MoveAction)
    temp_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    temp_table.viewport().setAcceptDrops(True)
    temp_table.setDragDropOverwriteMode(False)
    temp_table.setSortingEnabled(True)
    temp_table.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)
    temp_table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
    temp_table.hideColumn(list(temp_table.model().get_data().columns).index("Selected"))

    user_combo_del = TableModels.ComboBoxDelegate(OutsideYT.app_settings.accounts.keys())
    access_combo_del = TableModels.ComboBoxDelegate(["Private", "On link", "Public"])
    temp_table.setItemDelegateForColumn(list(temp_table.model().get_data().columns).index("User"), user_combo_del)
    temp_table.setItemDelegateForColumn(list(temp_table.model().get_data().columns).index("Access"), access_combo_del)


def update_upload():
    global Upload_table
    Upload_table = ui.Upload_Table
    Upload_table.verticalHeader().setSectionsMovable(True)
    ui.Upload_Progress_Bar.setVisible(False)
    Upload_table.setColumnCount(15)
    Upload_table.setHorizontalHeaderLabels(["id", "User", "Title", "Publ time", "Video", "Description",
                                            "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
                                            "Save title?", "Delete", "Selected"])
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

    ui.Download_SavingPath_Label.setText(OutsideYT.app_settings.vids_folder)
    ui.Download_Progress_Bar.setVisible(False)

    Download_table = ui.Download_Table
    Download_table.setColumnCount(5)
    Download_table.setHorizontalHeaderLabels(["Channel", "Video", "Folder", "Delete", "Select"])


def start_GUI():
    global app, YouTubeOutside, ui, Upload_table, Download_table, Watch_table, temp_table
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
