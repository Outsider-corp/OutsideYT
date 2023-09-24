from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget

import OutsideYT
from outside import TableModels as CommonTables
from outside import main_dialogs

from ..functions import update_checkbox_select_all
from ..YT_functions import upload_video
from . import TableModels, context_menu, dialogs


def update_upload(ui, parent):
    upload_table = ui.Upload_Table
    upload_model = TableModels.UploadModel(oldest_settings=ui,
                                           main_progress_bar=ui.Upload_Progress_Bar)
    upload_table.setModel(upload_model)

    upload_table = CommonTables.table_universal(upload_table)
    upload_table.hideColumn(list(upload_table.model().get_data().columns).index('Selected'))
    upload_table.setVerticalHeader(CommonTables.HeaderView(upload_table))
    upload_table.horizontalHeader().setFont(QtGui.QFont('Arial', 12))
    for i, size in enumerate([50, 0, 100, 250, 150]):
        upload_table.setColumnWidth(i, size)
    upload_table.setColumnWidth(11, 70)
    upload_table.setColumnWidth(12, 70)

    user_combo_del = CommonTables.ComboBoxDelegate(upload_table,
                                                   OutsideYT.app_settings_uploaders.accounts.keys())
    upload_table.setItemDelegateForColumn(
        list(upload_table.model().get_data().columns).index('User'), user_combo_del)

    access_combo_del = CommonTables.ComboBoxDelegate(upload_table,
                                                     ['Private', 'On link', 'Public'])
    upload_table.setItemDelegateForColumn(
        list(upload_table.model().get_data().columns).index('Access'),
        access_combo_del)
    upload_table.setItemDelegateForColumn(4, dialogs.SetPublishTimeDelegate(parent=parent,
                                                                            table=upload_table))
    upload_table.setItemDelegateForColumn(5, TableModels.OpenFileLocationDelegate(parent=parent,
                                                                                  table=upload_table,
                                                                                  ext='Video'))
    upload_table.setItemDelegateForColumn(8, TableModels.OpenFileLocationDelegate(parent=parent,
                                                                                  table=upload_table,
                                                                                  ext='Preview'))
    ends_combo_del = CommonTables.ComboBoxDelegate(upload_table, ['random', 'import'])
    upload_table.setItemDelegateForColumn(
        list(upload_table.model().get_data().columns).index('Ends'), ends_combo_del)

    cards_spin_del = CommonTables.SpinBoxDelegate(upload_table)
    upload_table.setItemDelegateForColumn(
        list(upload_table.model().get_data().columns).index('Cards'), cards_spin_del)

    ui.Upload_SelectVideos_Button.clicked.connect(
        partial(dialogs.open_upload_select_videos, parent=parent, table=upload_table))
    ui.Upload_Check_Button.clicked.connect(
        partial(dialogs.scan_videos_folder, table=upload_table))
    ui.Upload_UploadTime_Button.clicked.connect(
        partial(dialogs.set_upload_time, parent=parent, table=upload_table))
    ui.Upload_Start.clicked.connect(
        partial(start_upload, dialog=parent, dialog_settings=ui, table=upload_table))
    ui.Upload_SelectAll_CheckBox.clicked.connect(partial(update_checkbox_select_all,
                                                         checkbox=ui.Upload_SelectAll_CheckBox,
                                                         table=upload_table))

    upload_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    upload_table.customContextMenuRequested.connect(
        lambda pos: context_menu.upload_context_menu(pos, parent=parent, table=upload_table))
    ui.Upload_ClearUTime_Button.clicked.connect(
        partial(dialogs.clear_upload_time, parent=parent, table=upload_table))

    ui.actionUploaders_2.triggered.connect(partial(main_dialogs.open_UsersList_Dialog,
                                                   parent=parent,
                                                   table_type='upload',
                                                   add_table_class=TableModels.UploadersUsersModel))

    return upload_table, ui


def start_upload(dialog, dialog_settings, table):
    # start_operation(dialog=dialog, dialog_settings=dialog_settings, page="UploadPage",
    #                 progress_bar=dialog_settings.Upload_Progress_Bar,
    #                 process=partial(upload_video, login="test_test", mail="outside.deal1",
    #                                 folder="Uploaders"),
    #                 total_steps=7)
    print('Start Upload!')
    current_tab = dialog_settings.OutsideYT.findChild(QWidget, 'UploadPage')
    tab_elements = current_tab.findChildren(QWidget)

    for el in tab_elements:
        el.setEnabled(False)

    for num, video in table.model().get_data().iterrows():
        upload_video(user=video['User'],
                     title=video['Title'],
                     publish=video['Publish'],
                     video=video['Video'],
                     description=video['Description'],
                     playlist=video['Playlist'],
                     preview=video['Preview'],
                     tags=video['Tags'],
                     ends=video['Ends'],
                     cards=video['Cards'],
                     access=video['Access'],
                     save_title=video['Save filename?'],
                     driver_headless=not dialog_settings.Upload_ShowBrowser_checkBox.isChecked()
                     )

    for el in tab_elements:
        el.setEnabled(True)
