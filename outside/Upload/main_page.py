from functools import partial

from PyQt5 import QtCore, QtGui

import OutsideYT
from outside import TableModels as CommonTables
from outside import main_dialogs
from .dialogs import update_uploads_delegate
from ..asinc_functions import Uploader

from ..functions import update_checkbox_select_all, change_enabled_tab_elements
from . import TableModels, context_menu, dialogs
from ..main_dialogs import update_progress_bar, update_progress_label, init_add_label_generator
from ..message_boxes import error_func


def update_upload(ui, parent):
    upload_table = ui.Upload_Table
    upload_model = TableModels.UploadModel(oldest_settings=ui,
                                           table_progress_bar=ui.Upload_Progress_Bar,
                                           table_progress_label=ui.Upload_Progress_Label)
    upload_table.setModel(upload_model)

    upload_table = CommonTables.table_universal(upload_table)
    upload_table.hideColumn(list(upload_table.model().get_data().columns).index('Selected'))
    upload_table.setVerticalHeader(CommonTables.HeaderView(upload_table))
    upload_table.horizontalHeader().setFont(QtGui.QFont('Arial', 12))
    for i, size in enumerate([50, 0, 100, 250, 150]):
        upload_table.setColumnWidth(i, size)
    upload_table.setColumnWidth(11, 70)
    upload_table.setColumnWidth(12, 70)

    update_uploads_delegate(upload_table)

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
        partial(start_upload, dialog_settings=ui, table=upload_table))
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
                                                   parent_settings=ui,
                                                   table_type='upload',
                                                   add_table_class=partial(CommonTables.UsersModel,
                                                                           table_type='upload')))

    return upload_table, ui


def start_upload(dialog_settings, table):
    def finish(thread):
        try:
            comp_info = thread.completed_tasks_info
            thread.quit()
            thread.wait(OutsideYT.WAIT_TIME_THREAD)
            table.model()._data["Selected"] = comp_info
            if not all(table.model()._data["Selected"]):
                dialog_settings.Upload_SelectAll_CheckBox.setChecked(False)
            dialog_settings.upload_thread = None
        except Exception as e:
            print(f"Error on uploading finish...\n{e}")
        finally:
            change_enabled_tab_elements(dialog_settings, 'Upload', True)

    data = table.model().get_data()
    if len(data) and any(data['Selected']):
        change_enabled_tab_elements(dialog_settings, 'Upload', False)
        data_list = data.to_dict(orient='records')
        dialog_settings.upload_thread = Uploader(videos=data_list,
                                                 driver_headless=(
                                                     not dialog_settings.Upload_ShowBrowser_checkBox.isChecked()))
        add_label_gen = init_add_label_generator(table)
        dialog_settings.upload_thread.finished.connect(
            partial(finish, dialog_settings.upload_thread))
        dialog_settings.upload_thread.update_progress_signal.connect(
            lambda x: update_progress_bar(table, x))
        dialog_settings.upload_thread.update_progress_label_signal.connect(
            lambda x: update_progress_label(table, x))
        dialog_settings.upload_thread.add_progress_label_signal.connect(
            lambda x, y: add_label_gen.send((x, y)))
        dialog_settings.upload_thread.error_signal.connect(lambda x: error_func(x))
        dialog_settings.upload_thread.start()

