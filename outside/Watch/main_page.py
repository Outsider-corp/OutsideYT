import time
from functools import partial

from PyQt5 import QtGui, QtCore

import OutsideYT
from . import dialogs
from . import TableModels
from . import context_menu
from outside import TableModels as CommonTables
from outside import main_dialogs as MainDialogs
from ..YT_functions import watching
from ..asinc_functions import start_operation, start_watch_operation, WatchProgress
from ..functions import update_checkbox_select_all
from ..message_boxes import error_func


def update_watch(ui, parent):
    watch_table = ui.Watch_Table
    Watch_model = TableModels.WatchModel(oldest_settings=ui)
    watch_table.setModel(Watch_model)

    watch_table = CommonTables.table_universal(watch_table)
    watch_table.hideColumn(list(watch_table.model().get_data().columns).index("Selected"))
    watch_table.setVerticalHeader(CommonTables.HeaderView(watch_table))
    watch_table.horizontalHeader().setFont(QtGui.QFont("Arial", 12))
    width = parent.width()
    for i, size in enumerate([50, 150, 70, 350, 150, 70, int(width) - 880]):
        watch_table.setColumnWidth(i, size)

    group_combo_del = CommonTables.ComboBoxDelegate(watch_table, OutsideYT.app_settings_watchers.groups.keys())
    watch_table.setItemDelegateForColumn(list(watch_table.model().get_data().columns).index("Watchers Group"),
                                         group_combo_del)

    ui.Watch_SelectVideos_Button.clicked.connect(
        partial(dialogs.open_watch_select_videos, parent=parent, table=watch_table, parent_settings=ui))

    ui.Watch_advanced_settings_Button.clicked.connect(
        partial(dialogs.open_advanced_settings, parent=parent, table=watch_table))

    ui.Watch_url_add_Button.clicked.connect(
        partial(dialogs.add_video_to_table, table=watch_table, textbox=ui.Watch_url_textBox))

    ui.Watch_Start.clicked.connect(partial(start_watch, dialog=parent, dialog_settings=ui, table=watch_table))

    ui.Watch_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                        checkbox=ui.Watch_SelectAll_CheckBox,
                                                        table=watch_table))

    watch_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    watch_table.customContextMenuRequested.connect(
        lambda pos: context_menu.watch_context_menu(pos, parent=parent, table=watch_table))

    ui.actionWatchers_2.triggered.connect(partial(MainDialogs.open_UsersList_Dialog, parent=parent, table_type="watch",
                                                  add_table_class=TableModels.WatchersUsersModel
                                                  ))

    return watch_table, ui


def start_watch(dialog, dialog_settings, table):
    for _, video in table.model().get_data().iterrows():
        group = video["Watchers Group"]
        users = OutsideYT.app_settings_watchers.groups[group].keys()
        if not users:
            error_func(f'Group "{group}" has 0 watchers', parent=dialog)
            continue
        total_steps = video["Duration"] * len(users)
        group_progress = WatchProgress(total_steps)
        for user in users:
            start_watch_operation(dialog=dialog, dialog_settings=dialog_settings, page="WatchPage",
                                  progress_bar=dialog_settings.Watch_Progress_Bar, group_progress=group_progress,
                                  process=partial(watching, url=video["Link"], duration=video["Duration"], user=user))


def example_process():
    for i in range(5):
        time.sleep(i + 2)
        print(i + 2)
        yield i + 1
