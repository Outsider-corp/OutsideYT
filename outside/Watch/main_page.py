import time
from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget

from outside import TableModels as CommonTables
from outside import main_dialogs as MainDialogs
from OutsideYT import app_settings_watchers

from ..asinc_functions import SeekThreads, WatchProgress, start_watch_operation, AsyncWatchThread
from ..functions import update_checkbox_select_all
from ..main_dialogs import open_watch_down_select_videos, add_video_to_table
from ..message_boxes import error_func
from ..YT_functions import watching
from . import TableModels, context_menu, dialogs
from ..views_py.SelectWatchVideos_Dialog import Ui_SelectVideos_Dialog


def update_watch(ui, parent):
    watch_table = ui.Watch_Table
    watch_model = TableModels.WatchModel(oldest_settings=ui)
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
                add_table_class=Ui_SelectVideos_Dialog, table_type="Watch"))

    ui.Watch_advanced_settings_Button.clicked.connect(
        partial(dialogs.open_advanced_settings, parent=parent, table=watch_table))

    ui.Watch_url_add_Button.clicked.connect(
        partial(add_video_to_table, table=watch_table, table_type="Watch", textbox=ui.Watch_url_textBox))

    ui.Watch_Start.clicked.connect(
        partial(start_watch, dialog=parent, dialog_settings=ui, table=watch_table))

    ui.Watch_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                        checkbox=ui.Watch_SelectAll_CheckBox,
                                                        table=watch_table))

    watch_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    watch_table.customContextMenuRequested.connect(
        lambda pos: context_menu.watch_context_menu(pos, parent=parent, table=watch_table))

    ui.actionWatchers_2.triggered.connect(
        partial(MainDialogs.open_UsersList_Dialog, parent=parent, table_type='watch',
                add_table_class=TableModels.WatchersUsersModel,
                ))

    return watch_table, ui


def start_watch(dialog, dialog_settings, table):
    dialog_settings.watch_threads = []
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

        if not dialog_settings.watch_threads:
            for el in tab_elements:
                el.setEnabled(False)
            dialog_settings.Watch_Table.hideColumn(
                list(dialog_settings.Watch_Table.model().get_data().columns).index('id'))
            dialog_settings.Watch_Table.setColumnHidden(
                list(dialog_settings.Watch_Table.model().get_data().columns).index('Progress'),
                False)

        total_steps = video['Duration'] * len(users)
        group_progress = WatchProgress(total_steps)
        progress_bar = partial(dialog_settings.Watch_Table.model().update_progress_bar, index=num,
                               viewport=dialog_settings.Watch_Table)

        # async_thread = AsyncWatchThread(dialog)

        for user in users:
            process = partial(watching,
                              url=video['Link'],
                              duration=video['Duration'],
                              user=user,
                              driver_headless=not dialog_settings.Watch_ShowBrowser_checkBox.
                              isChecked(),
                              progress_bar=None)

            start_watch_operation(dialog_settings=dialog_settings,
                                  progress_bar=progress_bar,
                                  group_progress=group_progress,
                                  process=process)

            # async_thread.add_video(process)
        # async_thread.start()

    def seek_ends(seek_thread):
        seek_thread.deleteLater()
        dialog_settings.Watch_Table.model().reset_progress_bars()

    seek_threads = SeekThreads(dialog_settings.watch_threads, tab_elements, dialog_settings)
    seek_threads.finished.connect(partial(seek_ends, seek_thread=seek_threads))
    seek_threads.start()


def example_process():
    for i in range(5):
        time.sleep(i + 2)
        print(i + 2)
        yield i + 1
