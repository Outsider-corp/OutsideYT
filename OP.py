import sys
import os

import OutsideYT
from outside.views_py.Outside_MainWindow import Ui_YouTubeOutside
from outside.views_py import UsersList_Dialog
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
        table = globals()[f'Upload_table']
        print(table.model().get_data().iloc[0])
        table.update()

    @classmethod
    def add_row(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        table = globals()[f'{current_page}_table']
        if current_page == "Upload":
            table.model().insertRows()
        table.update()

    @classmethod
    def login_google(cls):
        table = globals()['Upload_table']
        login = table.model().get_data().loc[0, "Title"]
        mail = table.model().get_data().loc[0, "Description"]
        YT_Uploader.google_login(login, mail)


def update_ui():
    update_upload()
    update_watch()
    update_download()
    ui.actionUploaders_2.triggered.connect(open_UsersList_Dialog)
    ui.actionWatchers_2.triggered.connect(open_Watchers_List_Dialog)


def update_upload():
    global Upload_table
    Upload_table = ui.Upload_Table
    Upload_model = TableModels.UploadModel()
    Upload_table.setModel(Upload_model)
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    Upload_table.setFont(font)
    Upload_table.setFrameShape(QtWidgets.QFrame.StyledPanel)
    Upload_table.setFrameShadow(QtWidgets.QFrame.Sunken)
    Upload_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
    Upload_table.setAlternatingRowColors(False)
    Upload_table.setTextElideMode(Qt.ElideRight)
    Upload_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    Upload_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    Upload_table.setGridStyle(Qt.SolidLine)
    Upload_table.horizontalHeader().setCascadingSectionResizes(False)
    Upload_table.horizontalHeader().setStretchLastSection(False)

    Upload_table.setVerticalHeader(TableModels.HeaderView(Upload_table))

    Upload_table.verticalHeader().setCascadingSectionResizes(False)
    Upload_table.verticalHeader().setStretchLastSection(False)
    Upload_table.verticalHeader().setSectionsMovable(True)
    Upload_table.setDragEnabled(True)
    Upload_table.setDropIndicatorShown(True)
    Upload_table.setDefaultDropAction(QtCore.Qt.MoveAction)
    Upload_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    Upload_table.viewport().setAcceptDrops(True)
    Upload_table.setDragDropOverwriteMode(False)
    Upload_table.setSortingEnabled(True)
    Upload_table.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)
    Upload_table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
    Upload_table.hideColumn(list(Upload_table.model().get_data().columns).index("Selected"))

    user_combo_del = TableModels.ComboBoxDelegate(Upload_table, OutsideYT.app_settings_uploaders.accounts.keys())
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("User"), user_combo_del)

    access_combo_del = TableModels.ComboBoxDelegate(Upload_table, ["Private", "On link", "Public"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Access"), access_combo_del)

    ends_combo_del = TableModels.ComboBoxDelegate(Upload_table, ["random", "import"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Ends"), ends_combo_del)

    cards_spin_del = TableModels.SpinBoxDelegate(Upload_table)
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Cards"), cards_spin_del)



class Upload:

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

    ui.Download_SavingPath_Label.setText(OutsideYT.app_settings_uploaders.vids_folder)
    ui.Download_Progress_Bar.setVisible(False)

    Download_table = ui.Download_Table
    Download_table.setColumnCount(5)
    Download_table.setHorizontalHeaderLabels(["Channel", "Video", "Folder", "Delete", "Select"])


def open_UsersList_Dialog():
    dialog, dialog_settings = userslist()
    dialog.setWindowTitle("Uploaders List")
    dialog_model = TableModels.UsersModel()
    dialog_settings.Users_Table.setModel(dialog_model)
    dialog.exec_()

def open_Watchers_List_Dialog():
    dialog, dialog_settings = userslist()
    dialog.setWindowTitle("Watchers List")
    dialog.exec_()

def userslist():
    dialog = QtWidgets.QDialog(YouTubeOutside)
    dialog.setStyle(QStyleFactory.create("Fusion"))
    dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    dialog_settings.setupUi(dialog)
    dialog_settings.addUser_Button.click()
    return dialog, dialog_settings

def start_GUI():
    global app, YouTubeOutside, ui, Upload_table, Download_table, Watch_table
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # QtWidgets.QDialog.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # QtWidgets.QDialog.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
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
