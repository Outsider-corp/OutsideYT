import glob
import os
from functools import partial

import TableModels
from PyQt5 import QtWidgets, QtGui
import OutsideYT
import YT_Uploader
from outside.views_py import UsersList_Dialog, AddAccount_Dialog


def open_UsersList_Dialog(parent):
    cookies_dir = os.path.join(os.path.dirname(OutsideYT.app_settings_uploaders.file), "uploaders")
    dialog, dialog_settings = userslist(parent)
    dialog.setWindowTitle("Uploaders List")
    dialog_model = TableModels.UsersModel()
    dialog_settings.Users_Table.setModel(dialog_model)
    dialog_settings.Users_Table.setItemDelegate(TableModels.InLineEditDelegate())
    dialog_settings.Users_Table = TableModels.table_universal(dialog_settings.Users_Table)
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
        cook.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
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


def open_Watchers_List_Dialog(parent):
    dialog, dialog_settings = userslist(parent)
    dialog.setWindowTitle("Watchers List")
    dialog.exec_()


def open_addUser_Dialog(parent: QtWidgets.QTableView, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
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


def userslist(parent):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    dialog_settings.setupUi(dialog)
    return dialog, dialog_settings