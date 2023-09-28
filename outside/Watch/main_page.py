import time
from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget

from outside import TableModels as CommonTables
from OutsideYT import app_settings_watchers

from ..asinc_functions import SeekThreads, WatchThread
from ..functions import update_checkbox_select_all
from ..main_dialogs import open_watch_down_select_videos, add_video_from_textbox, \
    open_UsersList_Dialog
from ..message_boxes import error_func
from . import TableModels, context_menu, dialogs
from ..views_py.SelectWatchVideos_Dialog import Ui_SelectVideos_Dialog


def update_watch(ui, parent):
    watch_table = ui.Watch_Table
    watch_model = TableModels.WatchModel(oldest_settings=ui,
                                         main_progress_bar=ui.Watch_Progress_Bar,
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
        list(watch_table.model().get_data().columns).index('Watchers Group'),
        group_combo_del)
    progress_del = TableModels.ProgressBarDelegate(parent)
    watch_table.setItemDelegateForColumn(1, progress_del)

    ui.Watch_SelectVideos_Button.clicked.connect(
        partial(open_watch_down_select_videos, parent=parent, table=watch_table, parent_settings=ui,
                add_table_class=Ui_SelectVideos_Dialog))

    ui.Watch_advanced_settings_Button.clicked.connect(
        partial(dialogs.open_advanced_settings, parent=parent, table=watch_table))

    ui.Watch_url_add_Button.clicked.connect(
        partial(add_video_from_textbox, table=watch_table, textbox=ui.Watch_url_textBox))

    ui.Watch_Start.clicked.connect(
        partial(start_watch, dialog=parent, dialog_settings=ui, table=watch_table))

    ui.Watch_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                        checkbox=ui.Watch_SelectAll_CheckBox,
                                                        table=watch_table))

    watch_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    watch_table.customContextMenuRequested.connect(
        lambda pos: context_menu.watch_context_menu(pos, parent=parent, table=watch_table))

    ui.actionWatchers_2.triggered.connect(
        partial(open_UsersList_Dialog, parent=parent, table_type='watch',
                add_table_class=TableModels.WatchersUsersModel,
                ))

    return watch_table, ui


def start_watch(dialog, dialog_settings, table):

    def finish_video(video):
            watch_threads_check.remove(video)

    watch_threads_check = []
    current_tab = dialog_settings.OutsideYT.findChild(QWidget, 'WatchPage')
    tab_elements = current_tab.findChildren(QWidget)

    for num, video in table.model().get_data().iterrows():
        group = video['Watchers Group']
        users = app_settings_watchers.groups[group].keys()
        if not users:
            error_func(f'Group "{group}" has 0 watchers', parent=dialog)
            continue
        if not video['Selected']:
            continue

        if not watch_threads_check:
            for el in tab_elements:
                el.setEnabled(False)
            dialog_settings.Watch_Table.hideColumn(
                list(dialog_settings.Watch_Table.model().get_data().columns).index('id'))
            dialog_settings.Watch_Table.setColumnHidden(
                list(dialog_settings.Watch_Table.model().get_data().columns).index('Progress'),
                False)

        watch_thread = WatchThread(table=table, table_row=num, parent=dialog,
                                   driver_headless=not dialog_settings.Watch_ShowBrowser_checkBox.
                                   isChecked())
        watch_threads_check.append(num)
        watch_thread.start()
        watch_thread.finished.connect(partial(finish_video, video=num))

    def seek_ends(seek_thread):
        seek_thread.deleteLater()
        dialog_settings.Watch_Table.model().reset_progress_bars()

    seek_threads = SeekThreads(watch_threads_check, tab_elements, dialog_settings)
    seek_threads.finished.connect(partial(seek_ends, seek_thread=seek_threads))
    seek_threads.start()
