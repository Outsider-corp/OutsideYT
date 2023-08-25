import glob
from functools import partial

import outside.Watch.TableModels
import outside.Watch.context_menu
from PyQt5 import QtWidgets, QtGui, QtCore
import OutsideYT
from outside.functions import update_combobox
from outside.views_py import EditWatchersGroups_Dialog


def edit_watchers_groups(parent, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = EditWatchersGroups_Dialog.Ui_GroupsList_Dialog()
    dialog_settings.setupUi(dialog)
    dialog_model = outside.Watch.TableModels.WatchersGroupsModel()
    dialog_settings.Groups_Table.setModel(dialog_model)
    dialog_settings.Groups_Table.horizontalHeader().setFont(QtGui.QFont("Arial", 14))
    width = dialog.width() - 30
    dialog_settings.Groups_Table.setColumnWidth(0, int(width * 0.1))
    dialog_settings.Groups_Table.setColumnWidth(1, int(width * 0.45))
    dialog_settings.Groups_Table.setColumnWidth(2, width - int(width * 0.55))
    dialog_settings.primary_state = dialog_settings.Groups_Table.model().get_data().copy()
    dialog_settings.Groups_Table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    dialog_settings.Groups_Table.customContextMenuRequested.connect(
        lambda pos: outside.Watch.context_menu.watchers_dialogs_menu(pos, parent=dialog,
                                                                     table=dialog_settings.Groups_Table))

    def cancel():
        if ([dialog_settings.Groups_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Groups_Table.model().rowCount())]
            != list(dialog_settings.primary_state.index)) or \
                not (dialog_settings.primary_state.equals(dialog_settings.Groups_Table.model().get_data().copy())):
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

    def add_group():
        if OutsideYT.app_settings_watchers.add_group(outside.Watch.TableModels.WatchersUsersModel.default_group):
            dialog_settings.Groups_Table.model().insertRows()
            dialog_settings.Groups_Table.update()

    dialog_settings.addGroup_Button.clicked.connect(add_group)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(partial(cancel))

    def save():
        new_data = dialog_settings.Groups_Table.model().get_data()
        if not new_data["New Group name"].isna().all():
            for ind, row in new_data.iterrows():
                if row.Group != row["New Group name"] and row["New Group name"]:
                    OutsideYT.app_settings_watchers.change_group_name(row.Group, row["New Group name"])
        dialog_settings.Groups_Table.model().reset_ids(
            [dialog_settings.Groups_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Groups_Table.model().rowCount())])
        dialog_settings.Groups_Table.model()._data = dialog_settings.Groups_Table.model().get_data().sort_values(
            by="id")
        parent_settings.Users_Table.model().update()
        items = [f"No default group", *list(OutsideYT.app_settings_watchers.groups.keys())]
        parent_settings.DefUser_ComboBox = update_combobox(
            parent_settings.DefUser_ComboBox, items, OutsideYT.app_settings_watchers.def_group)
        dialog.accept()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)
    dialog.exec_()
