from functools import partial

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QTableView

from OutsideYT import app_settings_uploaders
from . import TableModels, context_menu
from outside import TableModels as CommonTables
from .dialogs import select_saving_path, open_advanced_settings
from .functions import _get_download_saving_path
from ..asinc_functions import DownloadThread
from ..functions import update_checkbox_select_all, update_combobox, get_video_link, \
    change_enabled_tab_elements
from ..main_dialogs import open_watch_down_select_videos, add_video_from_textbox
from ..message_boxes import error_func
from ..views_py.SelectDownloadVideos_Dialog import Ui_Download_Videos_Dialog


def update_download(ui, parent):
    def show_down_elements(mode: str):
        state = mode == 'user'
        ui.Download_Save_to_ComboBox.setVisible(state)
        ui.Download_Save_textBox.setVisible(not state)
        ui.Download_Select_Path_Button.setVisible(not state)

    download_table = ui.Download_Table
    download_model = TableModels.DownloadModel(oldest_settings=ui,
                                               table_progress_bar=ui.Download_Progress_Bar,
                                               table_progress_label=ui.Download_Progress_Label)
    download_table.setModel(download_model)
    download_table = CommonTables.table_universal(download_table)
    download_table.hideColumn(list(download_table.model().get_data().columns).index('Selected'))
    download_table.setVerticalHeader(CommonTables.HeaderView(download_table))
    download_table.horizontalHeader().setFont(QtGui.QFont('Arial', 12))
    width = parent.width()
    for i, size in enumerate([50, 400, 200, 70, int(width) - 760]):
        download_table.setColumnWidth(i, size)

    ui.Download_advanced_settings_Button.clicked.connect(
        partial(open_advanced_settings, parent=parent, table=download_table))

    ui.Download_SelectVideos_Button.clicked.connect(
        partial(open_watch_down_select_videos, parent=parent, table=download_table,
                parent_settings=ui,
                add_table_class=Ui_Download_Videos_Dialog))

    ui.Download_url_add_Button.clicked.connect(
        partial(add_video_from_textbox, table=download_table, textbox=ui.Download_url_textBox,
                dialog_settings=ui))

    ui.Download_Start.clicked.connect(
        partial(start_download, dialog=parent, dialog_settings=ui, table=download_table))

    ui.Download_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                           checkbox=ui.Download_SelectAll_CheckBox,
                                                           table=download_table))

    download_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    download_table.customContextMenuRequested.connect(
        lambda pos: context_menu.download_context_menu(pos, parent=parent, table=download_table))
    ui.Download_Save_to_ComboBox = update_combobox(ui.Download_Save_to_ComboBox,
                                                   app_settings_uploaders.accounts,
                                                   app_settings_uploaders.def_account)
    ui.Download_Select_Path_Button.clicked.connect(partial(select_saving_path, dialog_settings=ui))

    ui.Download_Folder_Save_Mode_radioButton.toggled.connect(lambda: show_down_elements('folder'))
    ui.Download_User_Save_Mode_radioButton.toggled.connect(lambda: show_down_elements('user'))
    show_down_elements('user' if ui.Download_User_Save_Mode_radioButton.isChecked() else 'folder')

    return download_table, ui


def start_download(dialog, dialog_settings, table: QTableView):
    def finish(thread):
        change_enabled_tab_elements(dialog_settings, 'DownloadPage', True)
        table.model().progress_label.clear()
        thread.deleteLater()

    data = table.model().get_data()
    try:
        saving_path = _get_download_saving_path(dialog_settings)
    except ValueError as e:
        error_func(text=e.args[0])
        return
    if len(data) and any(data['Selected']) and any(
            [dialog_settings.Download_Info_checkBox.isChecked(),
             dialog_settings.Download_Video_checkBox.isChecked()]):

        change_enabled_tab_elements(dialog_settings, 'DownloadPage', False)

        links = [get_video_link(i) for i in table.model().get_data()['Link'].to_list()]
        download_thread = DownloadThread(table=table, dialog=dialog,
                                         dialog_settings=dialog_settings,
                                         saving_path=saving_path,
                                         tasks=links, progress_bar=table.model().progress_bar,
                                         cards=True,
                                         download_info=dialog_settings.
                                         Download_Info_checkBox.isChecked(),
                                         download_videos=dialog_settings.
                                         Download_Video_checkBox.isChecked())

        download_thread.finished.connect(partial(finish, download_thread))
        download_thread.start()

