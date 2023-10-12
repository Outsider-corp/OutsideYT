import time
from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QWidget, QTableView

import OutsideYT
from outside import TableModels as CommonTables
from OutsideYT import app_settings_watchers

from ..asinc_functions import WatchManager
from ..functions import update_checkbox_select_all, change_enabled_tab_elements
from ..main_dialogs import open_watch_down_select_videos, add_video_from_textbox, \
    open_UsersList_Dialog
from ..message_boxes import error_func
from . import TableModels, context_menu, dialogs
from ..views_py.SelectWatchVideos_Dialog import Ui_SelectVideos_Dialog


def update_watch(ui, parent):
    watch_table = ui.Watch_Table
    watch_model = TableModels.WatchModel(oldest_settings=ui,
                                         table_progress_bar=ui.Watch_Progress_Bar,
                                         table_progress_label=ui.Watch_Progress_Label,
                                         tableview=watch_table)
    watch_table.setModel(watch_model)
    watch_table = CommonTables.table_universal(watch_table)
    watch_table.hideColumn(list(watch_table.model().get_data().columns).index('Selected'))
    watch_table.hideColumn(list(watch_table.model().get_data().columns).index('Progress'))
    watch_table.setVerticalHeader(CommonTables.HeaderView(watch_table))
    watch_table.horizontalHeader().setFont(QtGui.QFont('Arial', 12))
    width = parent.width()
    for i, size in enumerate([50, 150, 150, 70, 350, 150, 70, int(width) - 880]):
        watch_table.setColumnWidth(i, size)

    group_combo_del = CommonTables.ComboBoxDelegate(watch_table,
                                                    app_settings_watchers.groups.keys())
    watch_table.setItemDelegateForColumn(
        list(watch_table.model().get_data().columns).index('Watchers Group'), group_combo_del)
    progress_del = TableModels.ProgressBarDelegate(parent)
    watch_table.setItemDelegateForColumn(1, progress_del)

    ui.Watch_SelectVideos_Button.clicked.connect(
        partial(open_watch_down_select_videos, parent=parent, table=watch_table, parent_settings=ui,
                add_table_class=Ui_SelectVideos_Dialog))

    ui.Watch_advanced_settings_Button.clicked.connect(
        partial(dialogs.open_advanced_settings, parent=parent, table=watch_table))

    ui.Watch_url_add_Button.clicked.connect(
        partial(add_video_from_textbox, table=watch_table, textbox=ui.Watch_url_textBox,
                dialog_settings=ui))

    ui.Watch_Start.clicked.connect(
        partial(start_watch, dialog=parent, dialog_settings=ui, table=watch_table))

    ui.Watch_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                        checkbox=ui.Watch_SelectAll_CheckBox,
                                                        table=watch_table))

    watch_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    watch_table.customContextMenuRequested.connect(
        lambda pos: context_menu.watch_context_menu(pos, parent=parent, table=watch_table))

    ui.actionWatchers_2.triggered.connect(
        partial(open_UsersList_Dialog, parent=parent,
                table_type=watch_table.model().table_type.lower(),
                add_table_class=TableModels.WatchersUsersModel ))

    return watch_table, ui


def start_watch(dialog, dialog_settings, table: QTableView):

    def chk_headless():
        return not dialog_settings.Watch_ShowBrowser_checkBox.isChecked()

    def update_progress_watch(id: int, val: int):
        table.model().update_progress_bar(id, val)

    def finish():
        change_enabled_tab_elements(dialog_settings, 'Watch', True)
        dialog_settings.Watch_Table.hideColumn(
            list(dialog_settings.Watch_Table.model().get_data().columns).index('Progress'))
        dialog_settings.Watch_Table.setColumnHidden(
            list(dialog_settings.Watch_Table.model().get_data().columns).index('id'), False)
        table.model().reset_progress_bars()

    data = table.model().get_data()
    if not (len(data) and any(data['Selected'])):
        error_func(f'0 videos selected for watching', parent=dialog)
        return

    change_enabled_tab_elements(dialog_settings, 'Watch', False)
    dialog_settings.Watch_Table.hideColumn(
        list(dialog_settings.Watch_Table.model().get_data().columns).index('id'))
    dialog_settings.Watch_Table.setColumnHidden(
        list(dialog_settings.Watch_Table.model().get_data().columns).index('Progress'),
        False)

    watch_manager = WatchManager(OutsideYT.MAX_THREADS_COUNT)
    watch_manager.update_progress_watcher_signal.connect(
        lambda id, val: update_progress_watch(id, val))
    watch_manager.finish_signal.connect(finish)

    sel_data = data.to_dict(orient='records')
    table.model().disable_unselected_progress_bars()

    for num, video in enumerate(sel_data):
        if not video['Selected']:
            continue
        group = video.get('Watchers Group', app_settings_watchers.def_group)
        users = list(app_settings_watchers.groups[group].keys())
        if not users:
            error_func(f'Group "{group}" has 0 watchers', parent=dialog)
            continue
        watch_manager.add_watcher(num, video, users,
                                  driver_headless=chk_headless(),
                                  auto_start=True)
