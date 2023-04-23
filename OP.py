import glob
import sys
import os
from functools import partial

import OutsideYT
from outside.views_py.Outside_MainWindow import Ui_YouTubeOutside
from outside.views_py import UsersList_Dialog, AddAccount_Dialog
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
    Upload_table.setItemDelegate(TableModels.InLineEditDelegate())
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    Upload_table.setFont(font)
    Upload_table = table_universal(Upload_table)
    Upload_table.hideColumn(list(Upload_table.model().get_data().columns).index("Selected"))
    Upload_table.setVerticalHeader(TableModels.HeaderView(Upload_table))
    Upload_table.horizontalHeader().setFont(QtGui.QFont("Arial", 12))
    user_combo_del = TableModels.ComboBoxDelegate(Upload_table, OutsideYT.app_settings_uploaders.accounts.keys())
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("User"), user_combo_del)

    access_combo_del = TableModels.ComboBoxDelegate(Upload_table, ["Private", "On link", "Public"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Access"),
                                          access_combo_del)

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
    cookies_dir = os.path.join(os.path.dirname(OutsideYT.app_settings_uploaders.file), "uploaders")
    dialog, dialog_settings = userslist()
    dialog.setWindowTitle("Uploaders List")
    dialog_model = TableModels.UsersModel()
    dialog_settings.Users_Table.setModel(dialog_model)
    dialog_settings.Users_Table.setItemDelegate(TableModels.InLineEditDelegate())
    dialog_settings.Users_Table = table_universal(dialog_settings.Users_Table)
    width = dialog.width() - 30
    dialog_settings.Users_Table.setColumnWidth(0, int(width * 0.1))
    dialog_settings.Users_Table.setColumnWidth(1, int(width * 0.3))
    dialog_settings.Users_Table.setColumnWidth(2, width - int(width * 0.1) - int(width * 0.3))
    dialog_settings.Users_Table.horizontalHeader().setFont(QtGui.QFont("Arial", 14))
    dialog_settings.DefUser_ComboBox = update_combobox(dialog_settings.DefUser_ComboBox,
                                                       ["No default account",
                                                        *OutsideYT.app_settings_uploaders.accounts.keys()])
    adduser = partial(open_addUser_Dialog, parent=dialog, parent_settings=dialog_settings)
    dialog_settings.addUser_Button.clicked.connect(adduser)
    dialog_settings.primary_state = [dialog_settings.DefUser_ComboBox.currentText(),
                                     dialog_settings.Users_Table.model().get_data().copy()]

    def chk_cookies():
        files = glob.glob(f'{cookies_dir}/*_cookies')
        cook = QtWidgets.QDialog(dialog)
        cook.setStyle(QStyleFactory.create("Fusion"))
        cook_settings = AddAccount_Dialog.Ui_AddUser_Dialog()
        cook_settings.setupUi(cook)
        cook_settings.Account_textbox.setEnabled(False)
        for file in files:
            filename = os.path.basename(file).replace("_cookies", "")
            if filename in list(OutsideYT.app_settings_uploaders.accounts.keys()):
                continue
            cook_settings.Account_textbox.setText(filename)

            def ok():
                OutsideYT.app_settings_uploaders.add_account({
                    filename: cook_settings.Gmail_textbox.text()})

            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(cook.reject)
            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)
            cook.exec_()
        dialog_settings.Users_Table.model().update()
        dialog_settings.DefUser_ComboBox = update_combobox(dialog_settings.DefUser_ComboBox,
                                                           ["No default account",
                                                            *OutsideYT.app_settings_uploaders.accounts.keys()])

    dialog_settings.CheckCookies_Button.clicked.connect(chk_cookies)

    def cancel():
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != dialog_settings.DefUser_ComboBox.currentText()) or \
                not (dialog_settings.primary_state[1].equals(dialog_settings.Users_Table.model().get_data().copy())):
            confirm = QtWidgets.QMessageBox()
            confirm.setText(f"Are you sure you want to cancel?\n"
                            f"All changes will be lost!")
            confirm.setWindowTitle("Confirmation")
            confirm.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm.setDefaultButton(QtWidgets.QMessageBox.No)
            result = confirm.exec_()
            if result == QtWidgets.QMessageBox.Yes:
                confirm.reject()
                dialog.reject()
        else:
            dialog.reject()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(cancel)

    def save():
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != dialog_settings.DefUser_ComboBox.currentText()) or \
                not (dialog_settings.primary_state[1].equals(dialog_settings.Users_Table.model().get_data().copy())):
            def_user = dialog_settings.DefUser_ComboBox.currentText()
            if def_user == "No default account":
                def_user = ""
            if def_user != OutsideYT.app_settings_uploaders.def_account:
                OutsideYT.app_settings_uploaders.add_def_account(def_user)
            for ind, file in dialog_settings.primary_state[1].iterrows():
                old = file.Account
                new = dialog_settings.Users_Table.model().get_data().loc[ind, "Account"]
                if old != new:
                    os.rename(os.path.join(cookies_dir, f'{old}_cookies'), os.path.join(cookies_dir, f'{new}_cookies'))
                    if old == OutsideYT.app_settings_uploaders.def_account:
                        OutsideYT.app_settings_uploaders.add_def_account(new)
            dialog_settings.Users_Table.model().reset_ids(
                [dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
                 range(dialog_settings.Users_Table.model().rowCount())])
            dialog_settings.Users_Table.model()._data = dialog_settings.Users_Table.model().get_data().sort_values(
                by="id")
            accs = dialog_settings.Users_Table.model().get_data().set_index("Account")["Gmail"].to_dict()
            OutsideYT.app_settings_uploaders.update_accounts(accs)

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)
    dialog.exec_()


def open_Watchers_List_Dialog():
    dialog, dialog_settings = userslist()
    dialog.setWindowTitle("Watchers List")
    dialog.exec_()


def open_addUser_Dialog(parent: QtWidgets.QTableView, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QStyleFactory.create("Fusion"))
    dialog_settings = AddAccount_Dialog.Ui_AddUser_Dialog()
    dialog_settings.setupUi(dialog)

    def ok():
        login = dialog_settings.Account_textbox.text()
        mail = dialog_settings.Gmail_textbox.text()
        if login in list(OutsideYT.app_settings_uploaders.accounts.keys()):
            TableModels.error_func("This account name is already used!")
        else:
            try:
                dialog.close()
                added = YT_Uploader.google_login(login, mail)
                if added:
                    OutsideYT.app_settings_uploaders.add_account({login: mail})
                    parent_settings.primary_state[1] = parent_settings.Users_Table.model().get_data().copy()
                    parent_settings.Users_Table.model().update()
                    parent_settings.DefUser_ComboBox = update_combobox(parent_settings.DefUser_ComboBox,
                                                                       ["No default account",
                                                                        *OutsideYT.app_settings_uploaders.accounts.keys()])
            except:
                TableModels.error_func("Error.")

    dialog.accept = ok
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog.exec_()


def update_combobox(combobox, items):
    combobox.clear()
    combobox.addItems(items)
    if OutsideYT.app_settings_uploaders.def_account != "":
        combobox.setCurrentIndex(list(OutsideYT.app_settings_uploaders.accounts.keys()).index(
            OutsideYT.app_settings_uploaders.def_account) + 1)
    else:
        combobox.setCurrentIndex(0)
    return combobox


def google_login(login, mail, parent: QtWidgets.QDialog):
    if login in list(OutsideYT.app_settings_uploaders.accounts.keys()):
        TableModels.error_func("This account name is already used!")
    else:
        try:
            YT_Uploader.google_login(login, mail)
            parent.parent().update()
        except:
            TableModels.error_func("Error.")


def userslist():
    dialog = QtWidgets.QDialog(YouTubeOutside)
    dialog.setStyle(QStyleFactory.create("Fusion"))
    dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    dialog_settings.setupUi(dialog)
    return dialog, dialog_settings


def table_universal(table):
    table.setFrameShape(QtWidgets.QFrame.StyledPanel)
    table.setFrameShadow(QtWidgets.QFrame.Sunken)
    table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
    table.setAlternatingRowColors(False)
    table.setTextElideMode(Qt.ElideRight)
    table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    table.setGridStyle(Qt.SolidLine)
    table.horizontalHeader().setCascadingSectionResizes(False)
    table.horizontalHeader().setStretchLastSection(False)
    table.verticalHeader().setCascadingSectionResizes(False)
    table.verticalHeader().setStretchLastSection(False)
    table.verticalHeader().setSectionsMovable(True)
    table.setDragEnabled(True)
    table.setDropIndicatorShown(True)
    table.setDefaultDropAction(QtCore.Qt.MoveAction)
    table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    table.viewport().setAcceptDrops(True)
    table.setDragDropOverwriteMode(False)
    table.verticalHeader().setDefaultAlignment(Qt.AlignVCenter)
    table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
    return table


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
