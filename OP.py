import sys
import os
from functools import partial

import OutsideYT
import outside.Upload.TableModels
import outside.Upload.context_menu
import outside.Upload.dialogs
import outside.Watch.TableModels
from outside.views_py.Outside_MainWindow import Ui_YouTubeOutside
from outside import TableModels, main_dialogs

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QStyleFactory, QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt


class QMainWindowPlus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shortcut1 = QShortcut(QKeySequence('F5'), self)
        self.shortcut1.activated.connect(QMainWindowPlus.table_update)

        self.shortcut2 = QShortcut(QKeySequence('Ctrl+Shift+E'), self)
        self.shortcut2.activated.connect(QMainWindowPlus.open_main_folder)

        self.shortcut3 = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcut3.activated.connect(QMainWindowPlus.add_row)

    @classmethod
    def open_main_folder(cls):
        os.startfile(os.getcwd())

    @classmethod
    def table_update(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        table = globals()[f'Upload_table']
        table.update()

    @classmethod
    def add_row(cls):
        current_page = ui.OutsideYT.tabText(ui.OutsideYT.currentIndex())
        table = globals()[f'{current_page}_table']
        if current_page == "Upload":
            table.model().insertRows()
        table.update()


def update_ui():
    update_upload()
    update_watch()
    update_download()
    ui.actionUploaders_2.triggered.connect(partial(main_dialogs.open_UsersList_Dialog, parent=YouTubeOutside,
                                                   table_settings=OutsideYT.app_settings_uploaders,
                                                   all_accounts=OutsideYT.app_settings_uploaders.accounts.keys(),
                                                   combo_items_default=OutsideYT.app_settings_uploaders.accounts.keys(),
                                                   def_type="account",
                                                   add_table_class=outside.Upload.TableModels.UploadersUsersModel
                                                   ))
    ui.actionWatchers_2.triggered.connect(partial(main_dialogs.open_UsersList_Dialog, parent=YouTubeOutside,
                                                  table_settings=OutsideYT.app_settings_watchers,
                                                  all_accounts=OutsideYT.app_settings_watchers.accounts,
                                                  combo_items_default=OutsideYT.app_settings_watchers.groups.keys(),
                                                  def_type="group",
                                                  add_table_class=outside.Watch.TableModels.WatchersUsersModel
                                                  ))
    ui.actionOpen_Main_Folder.triggered.connect(QMainWindowPlus.open_main_folder)


def update_upload():
    global Upload_table
    Upload_table = ui.Upload_Table
    Upload_model = outside.Upload.TableModels.UploadModel()
    Upload_table.setModel(Upload_model)
    Upload_table.setItemDelegate(TableModels.InLineEditDelegate())
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    Upload_table.setFont(font)
    Upload_table = TableModels.table_universal(Upload_table)
    Upload_table.hideColumn(list(Upload_table.model().get_data().columns).index("Selected"))
    Upload_table.setVerticalHeader(TableModels.HeaderView(Upload_table))
    Upload_table.horizontalHeader().setFont(QtGui.QFont("Arial", 12))
    user_combo_del = TableModels.ComboBoxDelegate(Upload_table, OutsideYT.app_settings_uploaders.accounts.keys())
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("User"), user_combo_del)

    access_combo_del = TableModels.ComboBoxDelegate(Upload_table, ["Private", "On link", "Public"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Access"),
                                          access_combo_del)
    Upload_table.setItemDelegateForColumn(4, outside.Upload.dialogs.SetPublishTimeDelegate(parent=YouTubeOutside,
                                                                                                  table=Upload_table))
    Upload_table.setItemDelegateForColumn(5, outside.Upload.TableModels.OpenFileLocationDelegate(parent=YouTubeOutside,
                                                                                                 table=Upload_table,
                                                                                                 ext="Video"))
    Upload_table.setItemDelegateForColumn(8, outside.Upload.TableModels.OpenFileLocationDelegate(parent=YouTubeOutside,
                                                                                                 table=Upload_table,
                                                                                                 ext="Preview"))
    ends_combo_del = TableModels.ComboBoxDelegate(Upload_table, ["random", "import"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Ends"), ends_combo_del)

    cards_spin_del = TableModels.SpinBoxDelegate(Upload_table)
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Cards"), cards_spin_del)

    ui.Upload_SelectVideos_Button.clicked.connect(
        partial(outside.Upload.dialogs.open_upload_select_videos, parent=YouTubeOutside, table=Upload_table))
    ui.Upload_Check_Button.clicked.connect(
        partial(outside.Upload.dialogs.scan_videos_folder, table=Upload_table))
    ui.Upload_UploadTime_Button.clicked.connect(
        partial(outside.Upload.dialogs.set_upload_time, parent=YouTubeOutside, table=Upload_table))
    Upload_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    Upload_table.customContextMenuRequested.connect(
        lambda pos: outside.Upload.context_menu.upload_context_menu(pos, parent=YouTubeOutside, table=Upload_table))
    ui.Upload_ClearUTime_Button.clicked.connect(
        partial(outside.Upload.dialogs.clear_upload_time, parent=YouTubeOutside, table=Upload_table))


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
