from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import outside.Watch.context_menu
import outside.Watch.TableModels
from outside.OYT_Settings import app_settings_watchers
from outside.functions import update_combobox
from outside.message_boxes import error_func, warning_func
from outside.views_py import EditWatchersGroups_Dialog


def edit_watchers_groups(parent, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    dialog_settings = EditWatchersGroups_Dialog.Ui_GroupsList_Dialog()
    dialog_settings.setupUi(dialog)
    dialog_model = outside.Watch.TableModels.WatchersGroupsModel()
    dialog_settings.Groups_Table.setModel(dialog_model)
    dialog_settings.Groups_Table.horizontalHeader().setFont(QtGui.QFont('Arial', 14))
    width = dialog.width() - 30
    dialog_settings.Groups_Table.setColumnWidth(0, int(width * 0.1))
    dialog_settings.Groups_Table.setColumnWidth(1, int(width * 0.45))
    dialog_settings.Groups_Table.setColumnWidth(2, width - int(width * 0.55))
    dialog_settings.primary_state = dialog_settings.Groups_Table.model().get_data().copy()
    dialog_settings.Groups_Table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    dialog_settings.Groups_Table.customContextMenuRequested.connect(
        lambda pos: outside.Watch.context_menu.watchers_group_dialogs_menu(pos, parent=dialog,
                                                                           table=dialog_settings.Groups_Table))

    def cancel():
        if ([dialog_settings.Groups_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Groups_Table.model().rowCount())]
            != list(dialog_settings.primary_state.index)) or \
                not (dialog_settings.primary_state.equals(
                    dialog_settings.Groups_Table.model().get_data().copy())):
            if warning_func(parent=parent, text=f'Are you sure you want to cancel?\n'
                                                f'All changes will be lost!'):
                dialog.reject()
        else:
            dialog.reject()

    def add_group():
        dialog_settings.Groups_Table.model().insertRows()
        dialog_settings.Groups_Table.update()

    dialog_settings.addGroup_Button.clicked.connect(add_group)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(
        partial(cancel))

    def save():
        new_data = dialog_settings.Groups_Table.model().get_data()
        if not new_data['New Group name'].isna().all():
            for ind, row in new_data.iterrows():
                if row.Group != row['New Group name'] and row['New Group name']:
                    app_settings_watchers.change_group_name(row.Group,
                                                            row['New Group name'])
        dialog_settings.Groups_Table.model().reset_ids(
            [dialog_settings.Groups_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Groups_Table.model().rowCount())])
        dialog_settings.Groups_Table.model()._data = dialog_settings.Groups_Table.model().get_data().sort_values(
            by='id')
        parent_settings.Users_Table.model().update()
        items = list(app_settings_watchers.groups.keys())
        parent_settings.Group_comboBox = update_combobox(
            parent_settings.Group_comboBox, items, app_settings_watchers.def_group)
        dialog.accept()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)
    dialog.exec_()


def open_advanced_settings(parent, table):
    error_func('This action will be add later...')
