from functools import partial

from PyQt5 import QtGui, QtCore

import OutsideYT
from . import dialogs
from . import TableModels
from . import context_menu
from outside import TableModels as CommonTables
from outside import main_dialogs as MainDialogs


def update_watch(ui, parent):
    global Watch_table

    Watch_table = ui.Watch_Table
    Watch_model = TableModels.WatchModel()
    Watch_table.setModel(Watch_model)

    ui.Watch_Progress_Bar.setVisible(False)
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(12)
    Watch_table.setFont(font)
    Watch_table = CommonTables.table_universal(Watch_table)
    Watch_table.hideColumn(list(Watch_table.model().get_data().columns).index("Selected"))
    Watch_table.setVerticalHeader(CommonTables.HeaderView(Watch_table))
    Watch_table.horizontalHeader().setFont(QtGui.QFont("Arial", 12))
    width = parent.width()
    for i, size in enumerate([50, 150, 70, 350, 150, int(width) - 810]):
        Watch_table.setColumnWidth(i, size)

    group_combo_del = CommonTables.ComboBoxDelegate(Watch_table, OutsideYT.app_settings_watchers.groups.keys())
    Watch_table.setItemDelegateForColumn(list(Watch_table.model().get_data().columns).index("Watchers Group"),
                                         group_combo_del)

    ui.Watch_SelectVideos_Button.clicked.connect(
        partial(dialogs.open_watch_select_videos, parent=parent))

    ui.Watch_advanced_settings_Button.clicked.connect(
        partial(dialogs.open_advanced_settings, parent=parent, table=Watch_table))

    Watch_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    Watch_table.customContextMenuRequested.connect(
        lambda pos: context_menu.watch_context_menu(pos, parent=parent, table=Watch_table))

    ui.actionWatchers_2.triggered.connect(partial(MainDialogs.open_UsersList_Dialog, parent=parent,
                                                  table_settings=OutsideYT.app_settings_watchers,
                                                  combo_items_default=OutsideYT.app_settings_watchers.groups.keys(),
                                                  def_type="group",
                                                  add_table_class=TableModels.WatchersUsersModel
                                                  ))

    return Watch_table, ui
