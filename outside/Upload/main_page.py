from functools import partial

from PyQt5 import QtGui, QtCore

import OutsideYT
from . import context_menu, dialogs, TableModels
from outside import main_dialogs as MainDialogs
from outside import TableModels as CommonTables


def update_upload(ui, parent):
    upload_table = ui.Upload_Table
    Upload_model = TableModels.UploadModel()
    upload_table.setModel(Upload_model)

    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(11)
    upload_table.setFont(font)
    
    upload_table = CommonTables.table_universal(upload_table)
    upload_table.hideColumn(list(upload_table.model().get_data().columns).index("Selected"))
    upload_table.setVerticalHeader(CommonTables.HeaderView(upload_table))
    upload_table.horizontalHeader().setFont(QtGui.QFont("Arial", 12))
    for i, size in enumerate([50, 0, 100, 250, 150]):
        upload_table.setColumnWidth(i, size)
    upload_table.setColumnWidth(11, 70)
    upload_table.setColumnWidth(12, 70)

    user_combo_del = CommonTables.ComboBoxDelegate(upload_table, OutsideYT.app_settings_uploaders.accounts.keys())
    upload_table.setItemDelegateForColumn(list(upload_table.model().get_data().columns).index("User"), user_combo_del)

    access_combo_del = CommonTables.ComboBoxDelegate(upload_table, ["Private", "On link", "Public"])
    upload_table.setItemDelegateForColumn(list(upload_table.model().get_data().columns).index("Access"),
                                          access_combo_del)
    upload_table.setItemDelegateForColumn(4, dialogs.SetPublishTimeDelegate(parent=parent,
                                                                            table=upload_table))
    upload_table.setItemDelegateForColumn(5, TableModels.OpenFileLocationDelegate(parent=parent,
                                                                                  table=upload_table,
                                                                                  ext="Video"))
    upload_table.setItemDelegateForColumn(8, TableModels.OpenFileLocationDelegate(parent=parent,
                                                                                  table=upload_table,
                                                                                  ext="Preview"))
    ends_combo_del = CommonTables.ComboBoxDelegate(upload_table, ["random", "import"])
    upload_table.setItemDelegateForColumn(list(upload_table.model().get_data().columns).index("Ends"), ends_combo_del)

    cards_spin_del = CommonTables.SpinBoxDelegate(upload_table)
    upload_table.setItemDelegateForColumn(list(upload_table.model().get_data().columns).index("Cards"), cards_spin_del)

    ui.Upload_SelectVideos_Button.clicked.connect(
        partial(dialogs.open_upload_select_videos, parent=parent, table=upload_table))
    ui.Upload_Check_Button.clicked.connect(
        partial(dialogs.scan_videos_folder, table=upload_table))
    ui.Upload_UploadTime_Button.clicked.connect(
        partial(dialogs.set_upload_time, parent=parent, table=upload_table))

    upload_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    upload_table.customContextMenuRequested.connect(
        lambda pos: context_menu.upload_context_menu(pos, parent=parent, table=upload_table))
    ui.Upload_ClearUTime_Button.clicked.connect(
        partial(dialogs.clear_upload_time, parent=parent, table=upload_table))

    ui.actionUploaders_2.triggered.connect(partial(MainDialogs.open_UsersList_Dialog, parent=parent,
                                                   table_settings=OutsideYT.app_settings_uploaders,
                                                   combo_items_default=OutsideYT.app_settings_uploaders.accounts.keys(),
                                                   def_type="account",
                                                   add_table_class=TableModels.UploadersUsersModel
                                                   ))

    return upload_table, ui
