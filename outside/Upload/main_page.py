from functools import partial

from PyQt5 import QtGui, QtCore

import OutsideYT
from . import context_menu, dialogs, TableModels
from outside import main_dialogs as MainDialogs
from outside import TableModels as CommonTables


def update_upload(ui, parent):
    Upload_table = ui.Upload_Table
    Upload_model = TableModels.UploadModel()
    Upload_table.setModel(Upload_model)
    Upload_table.setItemDelegate(CommonTables.InLineEditDelegate())
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    Upload_table.setFont(font)
    Upload_table = CommonTables.table_universal(Upload_table)
    Upload_table.hideColumn(list(Upload_table.model().get_data().columns).index("Selected"))
    Upload_table.setVerticalHeader(CommonTables.HeaderView(Upload_table))
    for i, size in enumerate([50, 0, 100, 250, 150]):
        Upload_table.setColumnWidth(i, size)
    Upload_table.setColumnWidth(11, 70)
    Upload_table.setColumnWidth(12, 70)
    Upload_table.horizontalHeader().setFont(QtGui.QFont("Arial", 12))
    user_combo_del = CommonTables.ComboBoxDelegate(Upload_table, OutsideYT.app_settings_uploaders.accounts.keys())
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("User"), user_combo_del)

    access_combo_del = CommonTables.ComboBoxDelegate(Upload_table, ["Private", "On link", "Public"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Access"),
                                          access_combo_del)
    Upload_table.setItemDelegateForColumn(4, dialogs.SetPublishTimeDelegate(parent=parent,
                                                                            table=Upload_table))
    Upload_table.setItemDelegateForColumn(5, TableModels.OpenFileLocationDelegate(parent=parent,
                                                                                  table=Upload_table,
                                                                                  ext="Video"))
    Upload_table.setItemDelegateForColumn(8, TableModels.OpenFileLocationDelegate(parent=parent,
                                                                                  table=Upload_table,
                                                                                  ext="Preview"))
    ends_combo_del = CommonTables.ComboBoxDelegate(Upload_table, ["random", "import"])
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Ends"), ends_combo_del)

    cards_spin_del = CommonTables.SpinBoxDelegate(Upload_table)
    Upload_table.setItemDelegateForColumn(list(Upload_table.model().get_data().columns).index("Cards"), cards_spin_del)

    ui.Upload_SelectVideos_Button.clicked.connect(
        partial(dialogs.open_upload_select_videos, parent=parent, table=Upload_table))
    ui.Upload_Check_Button.clicked.connect(
        partial(dialogs.scan_videos_folder, table=Upload_table))
    ui.Upload_UploadTime_Button.clicked.connect(
        partial(dialogs.set_upload_time, parent=parent, table=Upload_table))
    Upload_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    Upload_table.customContextMenuRequested.connect(
        lambda pos: context_menu.upload_context_menu(pos, parent=parent, table=Upload_table))
    ui.Upload_ClearUTime_Button.clicked.connect(
        partial(dialogs.clear_upload_time, parent=parent, table=Upload_table))

    ui.actionUploaders_2.triggered.connect(partial(MainDialogs.open_UsersList_Dialog, parent=parent,
                                                   table_settings=OutsideYT.app_settings_uploaders,
                                                   combo_items_default=OutsideYT.app_settings_uploaders.accounts.keys(),
                                                   def_type="account",
                                                   add_table_class=TableModels.UploadersUsersModel
                                                   ))

    return Upload_table, ui
