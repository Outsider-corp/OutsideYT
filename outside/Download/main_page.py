from functools import partial

from PyQt5 import QtGui, QtCore

import OutsideYT
from . import TableModels, context_menu, dialogs
from outside import TableModels as CommonTables
from ..functions import update_checkbox_select_all
from ..main_dialogs import open_watch_down_select_videos, add_video_from_textbox
from ..views_py.SelectDownloadVideos_Dialog import Ui_Download_Videos_Dialog


def update_download(ui, parent):
    download_table = ui.Download_Table
    download_model = TableModels.DownloadModel(oldest_settings=ui,
                                               main_progress_bar=ui.Download_Progress_Bar)
    download_table.setModel(download_model)
    download_table = CommonTables.table_universal(download_table)
    download_table.hideColumn(list(download_table.model().get_data().columns).index('Selected'))
    download_table.setVerticalHeader(CommonTables.HeaderView(download_table))
    download_table.horizontalHeader().setFont(QtGui.QFont('Arial', 12))
    width = parent.width()
    for i, size in enumerate([50, 400, 200, 70, int(width) - 760]):
        download_table.setColumnWidth(i, size)

    # ui.Download_advanced_settings_Button.clicked.connect(
    #     partial(dialogs.open_advanced_settings, parent=parent, table=download_table))

    ui.Download_SelectVideos_Button.clicked.connect(
        partial(open_watch_down_select_videos, parent=parent, table=download_table,
                parent_settings=ui,
                add_table_class=Ui_Download_Videos_Dialog)
    )

    ui.Download_url_add_Button.clicked.connect(
        partial(add_video_from_textbox, table=download_table, textbox=ui.Download_url_textBox))

    ui.Watch_Start.clicked.connect(
        partial(start_download, dialog=parent, dialog_settings=ui, table=download_table))

    ui.Download_ChangePath_Button.clicked.connect(
        partial(dialogs.change_saving_path, dialog_settings=ui))

    ui.Download_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                           checkbox=ui.Download_SelectAll_CheckBox,
                                                           table=download_table))

    ui.Download_SavingPath_Label.setText(OutsideYT.app_settings_uploaders.vids_folder)

    download_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    download_table.customContextMenuRequested.connect(
        lambda pos: context_menu.download_context_menu(pos, parent=parent, table=download_table))

    return download_table, ui


def start_download():
    pass
