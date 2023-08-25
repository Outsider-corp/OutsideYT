import glob
import os
from functools import partial

import outside.Upload.context_menu
from outside import TableModels
from PyQt5 import QtWidgets, QtGui, QtCore
import OutsideYT
from outside.functions import update_combobox
from outside.errors import error_func
from outside.Upload.dialogs import google_login
from outside.views_py import UsersList_Dialog, WatchersList_Dialog, AddAccount_Dialog, AddWatcher_Dialog
from outside.Watch.dialogs import edit_watchers_groups


def open_UsersList_Dialog(parent, table_settings, table_name: str, all_accounts: list, combo_items_default: list,
                          def_type: str,
                          add_table_class):
    cookies_dir = os.path.join(os.path.dirname(OutsideYT.app_settings_uploaders.file), table_name.lower())
    dialog, dialog_settings = userslist(parent, table_name)
    dialog.setWindowTitle(f"{table_name.capitalize()} List")
    dialog_model = add_table_class()
    dialog_settings.Users_Table.setModel(dialog_model)
    dialog_settings.Users_Table.setItemDelegate(TableModels.InLineEditDelegate())
    dialog_settings.Users_Table = TableModels.table_universal(dialog_settings.Users_Table)
    dialog_settings.Users_Table.horizontalHeader().setFont(QtGui.QFont("Arial", 14))
    width = dialog.width() - 30
    if table_name.lower() == "uploaders":
        dialog_settings.Users_Table.setColumnWidth(0, int(width * 0.1))
        dialog_settings.Users_Table.setColumnWidth(1, int(width * 0.3))
        dialog_settings.Users_Table.setColumnWidth(2, width - int(width * 0.1) - int(width * 0.3))
        items = [f"No default {def_type}", *combo_items_default]
        dialog_settings.DefUser_ComboBox = update_combobox(
            dialog_settings.DefUser_ComboBox, items, OutsideYT.app_settings_uploaders.def_account)
    else:
        dialog_settings.Users_Table.setColumnWidth(0, int(width * 0.05))
        dialog_settings.Users_Table.setColumnWidth(1, int(width * 0.3))
        dialog_settings.Users_Table.setColumnWidth(2, width - int(width * 0.05) - int(width * 0.3) - int(width * 0.2))
        dialog_settings.Users_Table.setColumnWidth(3, int(width * 0.2))
        items = [f"No default {def_type}", *combo_items_default]
        dialog_settings.DefUser_ComboBox = update_combobox(
            dialog_settings.DefUser_ComboBox, items, OutsideYT.app_settings_watchers.def_group)
    adduser = partial(open_addUsers_Dialog, parent=dialog, parent_settings=dialog_settings,
                      table_settings=table_settings,
                      def_type=def_type, combo_items_default=combo_items_default,
                      dialog_ui=AddAccount_Dialog.Ui_AddUser_Dialog if table_name.lower() == "uploaders"
                      else AddWatcher_Dialog.Ui_AddUser_Dialog)
    dialog_settings.addUser_Button.clicked.connect(adduser)
    dialog_settings.primary_state = [dialog_settings.DefUser_ComboBox.currentText(),
                                     dialog_settings.Users_Table.model().get_data().copy()]
    dialog_settings.Users_Table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    dialog_settings.Users_Table.customContextMenuRequested.connect(
        lambda pos: outside.Upload.context_menu.uploaders_dialogs_menu(pos, parent=dialog,
                                                                       table=dialog_settings.Users_Table))

    def chk_cookies():
        files = glob.glob(f'{cookies_dir}/*_cookies')
        cook = QtWidgets.QDialog(dialog)
        cook.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        cook_settings = AddAccount_Dialog.Ui_AddUser_Dialog()
        cook_settings.setupUi(cook)
        cook_settings.Account_textbox.setEnabled(False)
        for file in files:
            filename = os.path.basename(file).replace("_cookies", "")
            if filename in all_accounts:
                continue
            cook_settings.Account_textbox.setText(filename)

            def ok():
                if hasattr(cook_settings, "Group_comboBox"):
                    OutsideYT.app_settings_watchers.add_account(cook_settings.Group_comboBox.currentText(),
                                                                {filename: cook_settings.Gmail_textbox.text()})
                else:
                    OutsideYT.app_settings_uploaders.add_account({filename: cook_settings.Gmail_textbox.text()})

            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(cook.reject)
            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)
            cook.exec_()
        dialog_settings.Users_Table.model().update()
        items = [f"No default {def_type}", *combo_items_default]
        dialog_settings.DefUser_ComboBox = update_combobox(
            dialog_settings.DefUser_ComboBox, items, OutsideYT.app_settings_watchers.def_group)

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

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(partial(cancel))

    def save():
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != dialog_settings.DefUser_ComboBox.currentText()) or \
                not (dialog_settings.primary_state[1].equals(dialog_settings.Users_Table.model().get_data().copy())):
            def_user = dialog_settings.DefUser_ComboBox.currentText()
            if def_user == f"No default {def_type}":
                getattr(table_settings, f'del_def_{def_type}')()
            if def_user != getattr(table_settings, f'def_{def_type}'):
                getattr(table_settings, f'add_def_{def_type}')(def_user)
            for ind, file in dialog_settings.primary_state[1].iterrows():
                old = file.Account
                old_group = file.Group if "Group" in file.columns else None
                if ind in dialog_settings.Users_Table.model().get_data().index:
                    new = dialog_settings.Users_Table.model().get_data().loc[ind, "Account"]
                    if table_name.lower() == "uploaders":
                        table_settings.edit_account(old, new)
                    else:
                        table_settings.edit_account(old_group, old,
                                                    dialog_settings.Users_Table.model().get_data().loc[ind, "Group"],
                                                    new)
                else:
                    table_settings.del_account(old_group, old)
            dialog_settings.Users_Table.model().reset_ids(
                [dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
                 range(dialog_settings.Users_Table.model().rowCount())])
            if table_name.lower() == "uploaders":
                dialog_settings.Users_Table.model()._data = dialog_settings.Users_Table.model().get_data().sort_values(
                    by="id")
                accs = dialog_settings.Users_Table.model().get_data().set_index("Account")["Gmail"].to_dict()
                OutsideYT.app_settings_uploaders.update_accounts(accs)
            else:
                dialog_settings.Users_Table.model()._data = dialog_settings.Users_Table.model().get_data().sort_values(
                    by="Group")
                data = {}
                for _, row in dialog_settings.Users_Table.model().get_data().iterrows():
                    group = row["Group"]
                    account = row["Account"]
                    gmail = row["Gmail"]
                    if group not in data:
                        data[group] = {}
                    data[group][account] = gmail
                OutsideYT.app_settings_watchers.update_groups(data)

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)
    if table_name.lower() == "watchers":
        dialog_settings.EditGroups_Button.clicked.connect(
            partial(edit_watchers_groups, parent=dialog, parent_settings=dialog_settings))
        dialog_settings.Users_Table.model().update()
        dialog.parent().update()
    dialog.exec_()


def open_addUsers_Dialog(parent: QtWidgets.QTableView, parent_settings, table_settings, def_type: str,
                         dialog_ui, combo_items_default: list):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = dialog_ui()
    dialog_settings.setupUi(dialog)

    def ok():
        login = dialog_settings.Account_textbox.text()
        mail = dialog_settings.Gmail_textbox.text()
        group = dialog_settings.Group_comboBox.currentText() if hasattr(dialog_settings, "Group_comboBox") else None
        if OutsideYT.app_settings_uploaders.find_account(login):
            error_func(f"This account name is already used!")
        else:
            try:
                dialog.close()
                added = google_login(login, mail, parent=dialog, table_settings=table_settings)
                if added:
                    table_settings.add_account(acc={login: mail}, group=group)
                    parent_settings.primary_state[1] = parent_settings.Users_Table.model().get_data().copy()
                    parent_settings.Users_Table.model().update()
                    items = [f"No default {def_type}", *combo_items_default]
                    dialog_settings.DefUser_ComboBox = update_combobox(
                        dialog_settings.DefUser_ComboBox, items, OutsideYT.app_settings_uploaders.def_account)
            except Exception as e:
                error_func(f"Error. \n{e}")

    dialog.accept = ok
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog.exec_()


def userslist(parent, table_name: str):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    if table_name.lower() == "uploaders":
        dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    else:
        dialog_settings = WatchersList_Dialog.Ui_WatchersList_Dialog()
    dialog_settings.setupUi(dialog)
    return dialog, dialog_settings
