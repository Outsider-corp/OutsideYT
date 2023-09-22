import glob
import os
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import outside.Upload.context_menu as upload_context
import outside.Watch.context_menu as watch_context
import OutsideYT
from outside import TableModels
from outside.YT_functions import select_page, get_video_info, get_playlist_info
from outside.asinc_functions import start_operation
from outside.functions import update_combobox
from outside.message_boxes import error_func, warning_func
from outside.Upload.dialogs import google_login
from outside.views_py import (
    AddUploader_Dialog,
    AddWatcher_Dialog,
    UsersList_Dialog,
    WatchersList_Dialog,
)
from outside.Watch.dialogs import edit_watchers_groups


def open_UsersList_Dialog(parent, table_type: str, add_table_class):
    if table_type == 'upload':
        table_settings = OutsideYT.app_settings_uploaders
        def_type = 'account'
        combo_items_default = table_settings.accounts.keys()
    elif table_type == 'watch':
        table_settings = OutsideYT.app_settings_watchers
        def_type = 'group'
        combo_items_default = table_settings.groups.keys()
    else:
        return
    table_settings.update_settings()
    cookies_dir = os.path.join(os.path.dirname(table_settings.file),
                               str(table_settings).lower())
    dialog, dialog_settings = userslist(parent, str(table_settings))
    dialog.setWindowTitle(f'{str(table_settings).capitalize()} List')
    dialog_model = add_table_class()
    dialog_settings.Users_Table.setModel(dialog_model)
    dialog_settings.Users_Table = TableModels.table_universal(dialog_settings.Users_Table,
                                                              font_size=12)
    dialog_settings.Users_Table.setItemDelegate(TableModels.InLineEditDelegate())
    dialog_settings.Users_Table.setVerticalHeader(
        TableModels.HeaderView(dialog_settings.Users_Table, replace=False))

    width = dialog.width() - 50
    if str(table_settings).lower() == 'uploaders':
        dialog_settings.Users_Table.setColumnWidth(0, int(width * 0.1))
        dialog_settings.Users_Table.setColumnWidth(1, int(width * 0.3))
        dialog_settings.Users_Table.setColumnWidth(2, width - int(width * 0.1) - int(width * 0.3))
        items = [f'No default {def_type}', *combo_items_default]
        dialog_settings.DefUser_ComboBox = update_combobox(
            dialog_settings.DefUser_ComboBox, items, table_settings.def_account)
        dialog_settings.primary_state = [dialog_settings.DefUser_ComboBox.currentText(),
                                         dialog_settings.Users_Table.model().get_data().copy()]
    else:
        dialog_settings.Users_Table.setColumnWidth(0, int(width * 0.05))
        dialog_settings.Users_Table.setColumnWidth(1, int(width * 0.25))
        dialog_settings.Users_Table.setColumnWidth(2, int(width * 0.45))
        dialog_settings.Users_Table.setColumnWidth(3, int(width * 0.25))
        dialog_settings.Group_comboBox = update_combobox(
            dialog_settings.Group_comboBox, combo_items_default,
            table_settings.def_group)
        groups_combo_del = TableModels.ComboBoxDelegate(
            dialog_settings.Users_Table,
            table_settings.groups.keys())
        dialog_settings.Users_Table.setItemDelegateForColumn(
            list(dialog_settings.Users_Table.model().get_data().columns).index('Group'),
            groups_combo_del)
        dialog_settings.primary_state = [dialog_settings.Group_comboBox.currentText(),
                                         dialog_settings.Users_Table.model().get_data().copy()]

    dialog_settings.Users_Table.horizontalHeader().setFont(QtGui.QFont('Arial', 14))

    adduser = partial(open_addUsers_Dialog, parent=dialog, parent_settings=dialog_settings,
                      table_settings=table_settings,
                      def_type=def_type, combo_items_default=combo_items_default,
                      dialog_ui=AddUploader_Dialog.Ui_AddUser_Dialog if str(
                          table_settings).lower() == 'uploaders'
                      else AddWatcher_Dialog.Ui_AddUser_Dialog)
    dialog_settings.addUser_Button.clicked.connect(adduser)
    dialog_settings.Users_Table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def context_menu(pos):
        if str(table_settings).lower() == 'uploaders':
            upload_context.uploaders_dialogs_menu(pos, parent=dialog,
                                                  table=dialog_settings.Users_Table)
        elif str(table_settings).lower() == 'watchers':
            watch_context.watchers_dialogs_menu(pos, parent=dialog,
                                                table=dialog_settings.Users_Table)

    dialog_settings.Users_Table.customContextMenuRequested.connect(lambda pos: context_menu(pos))

    def cancel():
        if hasattr(dialog_settings, 'Group_comboBox'):
            box = dialog_settings.Group_comboBox
        else:
            box = dialog_settings.DefUser_ComboBox
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != box.currentText()) or \
                not (dialog_settings.primary_state[1].equals(
                    dialog_settings.Users_Table.model().get_data().copy())):
            if warning_func(f'Are you sure you want to cancel?\n'
                            f'All changes will be lost! (except add/remove', parent):
                dialog.reject()
        else:
            dialog.reject()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(
        partial(cancel))

    def save():
        if hasattr(dialog_settings, 'Group_comboBox'):
            box = dialog_settings.Group_comboBox
        else:
            box = dialog_settings.DefUser_ComboBox
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != box.currentText()) or \
                not (dialog_settings.primary_state[1].equals(
                    dialog_settings.Users_Table.model().get_data())):
            def_user = box.currentText()
            if def_user == f'No default {def_type}':
                getattr(table_settings, f'del_def_{def_type}')()
            if def_user != getattr(table_settings, f'def_{def_type}'):
                getattr(table_settings, f'add_def_{def_type}')(def_user)
            for ind, file in dialog_settings.primary_state[1].iterrows():
                old = file.Account
                old_group = None
                if ind in dialog_settings.Users_Table.model().get_data().index:
                    new = dialog_settings.Users_Table.model().get_data().loc[ind, 'Account']
                    if str(table_settings).lower() == 'uploaders':
                        if old != new:
                            table_settings.edit_account(old, new)
                    elif str(table_settings).lower() == 'watchers':
                        old_group = file.Group
                        new_group = dialog_settings.Users_Table.model().get_data().loc[ind, 'Group']
                        if old != new or old_group != new_group:
                            table_settings.edit_account(old_group, old, new_group, new)
                else:
                    table_settings.del_account(group=old_group, login=old, parent=parent)
            dialog_settings.Users_Table.model().reset_ids(
                [dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
                 range(dialog_settings.Users_Table.model().rowCount())])
            if str(table_settings).lower() == 'uploaders':
                dialog_settings.Users_Table.model()._data = \
                    dialog_settings.Users_Table.model().get_data().sort_values(by='id')
                accs = dialog_settings.Users_Table.model().get_data().set_index('Account')[
                    'Gmail'].to_dict()
                table_settings.update_accounts(accs)
            else:
                dialog_settings.Users_Table.model()._data = \
                    dialog_settings.Users_Table.model().get_data().sort_values(by='Group')
                data = {}
                for _, row in dialog_settings.Users_Table.model().get_data().iterrows():
                    group = row['Group']
                    account = row['Account']
                    gmail = row['Gmail']
                    if group not in data:
                        data[group] = {}
                    data[group][account] = gmail
                table_settings.update_groups(data)

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)

    def chk_cookies(dialog_settings):
        def ok(filename, cook_settings):
            if hasattr(cook_settings, 'Group_comboBox'):
                table_settings.add_account(
                    group=cook_settings.Group_comboBox.currentText(),
                    acc={filename: cook_settings.Gmail_textbox.text()})
            else:
                table_settings.add_account(
                    {filename: cook_settings.Gmail_textbox.text()})

        files = glob.glob(f'{cookies_dir}/*_cookies')
        all_accounts = table_settings.accounts
        for file in files:
            filename = os.path.basename(file).replace('_cookies', '')
            if filename in all_accounts:
                continue

            cook = QtWidgets.QDialog(dialog)
            cook.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
            if str(table_settings).lower() == 'uploaders':
                cook_settings = AddUploader_Dialog.Ui_AddUser_Dialog()
                cook_settings.setupUi(cook)
            else:
                cook_settings = AddWatcher_Dialog.Ui_AddUser_Dialog()
                cook_settings.setupUi(cook)
                cook_settings.Group_comboBox = update_combobox(cook_settings.Group_comboBox,
                                                               combo_items_default,
                                                               table_settings.def_group)
            cook_settings.Account_textbox.setEnabled(False)
            cook_settings.Account_textbox.setText(filename)

            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(
                cook.reject)
            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(
                partial(ok, filename=filename, cook_settings=cook_settings))
            cook.exec_()

        dialog.close()
        open_UsersList_Dialog(parent, table_type, add_table_class)

        # dialog_settings.Users_Table.model().update()
        # items = [f"No default {def_type}", *combo_items_default]
        # dialog_settings = update_settings_combobox_with_type(dialog_settings, items)

    dialog_settings.CheckCookies_Button.clicked.connect(
        partial(chk_cookies, dialog_settings=dialog_settings))

    if str(table_settings).lower() == 'watchers':
        dialog_settings.EditGroups_Button.clicked.connect(
            partial(edit_watchers_groups, parent=dialog, parent_settings=dialog_settings))
        dialog_settings.Users_Table.model().update()
        dialog.parent().update()
    dialog.exec_()


def open_addUsers_Dialog(parent: QtWidgets.QTableView, parent_settings, table_settings,
                         def_type: str,
                         dialog_ui, combo_items_default: list):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    dialog_settings = dialog_ui()
    dialog_settings.setupUi(dialog)
    items = [f'No {def_type}', *combo_items_default]
    dialog_settings = update_settings_combobox_with_type(dialog_settings, items)

    def ok(parent_settings):
        login = dialog_settings.Account_textbox.text()
        mail = dialog_settings.Gmail_textbox.text()
        group = dialog_settings.Group_comboBox.currentText() if hasattr(dialog_settings,
                                                                        'Group_comboBox') else None
        if table_settings.find_account(login):
            error_func(f'This account name is already used!')
        else:
            try:
                dialog.close()
                added = google_login(login, mail, parent=dialog, table_settings=table_settings)
                if added:
                    table_settings.add_account(acc={login: mail}, group=group)

                    parent_settings.primary_state[
                        1] = parent_settings.Users_Table.model().get_data().copy()
                    parent_settings.Users_Table.model().update()
                    items = [f'No default {def_type}', *combo_items_default]
                    parent_settings = update_settings_combobox_with_type(
                        dialog_settings=parent_settings,
                        items=items)
            except Exception as e:
                error_func(f'Error. \n{e}')

    dialog.accept = partial(ok, parent_settings=parent_settings)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(
        dialog.reject)
    dialog.exec_()


def open_watch_down_select_videos(parent, table: QtWidgets.QTableView, parent_settings, add_table_class,
                                  table_type: str):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    dialog_settings = add_table_class()
    dialog_settings.setupUi(dialog)

    radios = [dialog_settings.Last_video_radioButton, dialog_settings.Random_video_radioButton,
              dialog_settings.Period_radioButton]
    var1 = [dialog_settings.Count_label, dialog_settings.Count_videos_spinBox]
    var2 = [dialog_settings.Start_label, dialog_settings.Start_date, dialog_settings.End_label,
            dialog_settings.End_date]

    def add_video():
        text = select_page('video')
        if text:
            if table_type == "Watch":
                group = dialog_settings.Group_comboBox.currentText()
                add_video_to_table(table, link=text, group=group)
            else:
                add_video_to_table(table, link=text)
            dialog.accept()
        else:
            error_func('Not valid link.', dialog)

    def add_playlist():
        error_func('This action will be add later...')
        # text = select_page("playlist")
        # if text:
        #     group = dialog_settings.Group_comboBox.currentText()
        #     add_video_to_table(table, text, group)
        #     dialog.accept()
        # else:
        #     error_func("Not valid link.", dialog)

    def import_links_from_file():
        exts = OutsideYT.text_extensions
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                                        f'Select File with Links', '',
                                                        f"Text Files ("
                                                        f"{' '.join('*' + ex for ex in exts)})")
        if not file:
            return

        group = dialog_settings.Group_comboBox.currentText() if table_type == "Watch" else None
        dialog.accept()

        with open(file, 'r', encoding='UTF-8') as f:
            links = f.readlines()
        for num, link in enumerate(links):
            add_video_to_table(table=table, link=link, group=group, table_type=table_type)
##################################################################################################
        # start_operation(
        #     dialog=parent,
        #     dialog_settings=parent_settings,
        #     page=f'{table_type}Page',
        #     progress_bar=getattr(parent_settings, f'{table_type}_Progress_Bar'),
        #     process=partial(import_links_process, file=file, table_type=table_type))
##################################################################################################


    def select_channel():
        text = select_page('channel')
        if text:
            dialog_settings.channel_link_textBox.setText(text)
        else:
            error_func('Not valid link.', dialog)

    def show_elements(group):
        """
        Args:
            group: str - "none" - hide all elements, "count" - show count elements and radios,
            "period" - show period elements and radios.
        """
        if group == 'none':
            for el in radios + var1 + var2:
                el.setVisible(False)
        elif group == 'count':
            for el in radios + var1:
                el.setVisible(True)
            for el in var2:
                el.setVisible(False)
        elif group == 'period':
            for el in radios + var2:
                el.setVisible(True)
            for el in var1:
                el.setVisible(False)

    def show_actions_for_channel():
        if dialog_settings.channel_link_textBox.text() == '':
            show_elements('none')
        else:
            show_elements('count')

    def ok():
        url = dialog_settings.channel_link_textBox.text()
        if url == '':
            dialog.reject()
        elif 'youtube.com/' not in url:
            error_func(f'Wrong url: {url}')
        else:
            if table_type == "Watch":
                group = dialog_settings.Group_comboBox.currentText()
            if dialog_settings.Last_video_radioButton.isChecked():
                dialog_settings.Count_videos_spinBox.value()

                # table.model().insertRows(row_content={"Watchers Group": group,
                #                                       "Video": video,
                #                                       "Channel": channel,
                #                                       "Link": link})

            elif dialog_settings.Random_video_radioButton.isChecked():
                dialog_settings.Count_videos_spinBox.value()
            else:
                dialog_settings.Start_date.time()
                dialog_settings.End_date.time()
    if table_type == "Watch":
        items = list(OutsideYT.app_settings_watchers.groups.keys())
        dialog_settings.Group_comboBox = update_combobox(
            dialog_settings.Group_comboBox, items, OutsideYT.app_settings_watchers.def_group)

    show_elements('none')
    dialog_settings.channel_link_textBox.textChanged.connect(show_actions_for_channel)
    dialog_settings.Last_video_radioButton.toggled.connect(lambda: show_elements('count'))
    dialog_settings.Random_video_radioButton.toggled.connect(lambda: show_elements('count'))
    dialog_settings.Period_radioButton.toggled.connect(lambda: show_elements('period'))

    dialog_settings.AddVideo_Button.clicked.connect(add_video)
    dialog_settings.AddPlaylist_Button.clicked.connect(add_playlist)
    dialog_settings.Import_links_Button.clicked.connect(import_links_from_file)
    dialog_settings.Select_channel_Button.clicked.connect(select_channel)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(
        dialog.reject)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)

    dialog.exec_()


def add_video_to_table(table, link: str = '', group=None, table_type: str = "Download",
                       textbox: QtWidgets.QLineEdit = None):
    if group is None and table_type == "Watch":
        group = OutsideYT.app_settings_watchers.def_group
    if not link:
        if not textbox:
            return
        link = textbox.text()
    if 'youtube.com/watch' in link or 'youtu.be/' in link:
        video, channel, duration = get_video_info(link)
        if video and channel and duration:
            if table_type == "Watch":
                table.model().insertRows(row_content={'Watchers Group': group,
                                                      'Video': video,
                                                      'Channel': channel,
                                                      'Duration': duration,
                                                      'Link': link})
            else:
                table.model().insertRows(row_content={'Video': video,
                                                      'Channel': channel,
                                                      'Duration': duration,
                                                      'Link': link})
    elif 'youtube.com/playlist' in link:
        videos = get_playlist_info(link)
        if videos:
            if table_type == "Watch":
                for video, channel, video_link in videos:
                    table.model().insertRows(row_content={'Watchers Group': group,
                                                          'Video': video,
                                                          'Channel': channel,
                                                          'Link': video_link})
            else:
                for video, channel, video_link in videos:
                    table.model().insertRows(row_content={'Video': video,
                                                          'Channel': channel,
                                                          'Link': video_link})
    else:
        return
    if textbox is not None:
        textbox.clear()
        table.update()


def userslist(parent, table_name: str):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    if table_name.lower() == 'uploaders':
        dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    else:
        dialog_settings = WatchersList_Dialog.Ui_WatchersList_Dialog()
    dialog_settings.setupUi(dialog)
    return dialog, dialog_settings


def update_settings_combobox_with_type(dialog_settings, items):
    if hasattr(dialog_settings, 'Group_comboBox'):
        dialog_settings.Group_comboBox = update_combobox(
            dialog_settings.Group_comboBox, items[1:], OutsideYT.app_settings_watchers.def_group)
    elif hasattr(dialog_settings, 'DefUser_ComboBox'):
        dialog_settings.DefUser_ComboBox = update_combobox(
            dialog_settings.DefUser_ComboBox, items, OutsideYT.app_settings_uploaders.def_account)
    return dialog_settings


def update_settings_from_file():
    OutsideYT.app_settings_uploaders.update_settings()
    OutsideYT.app_settings_watchers.update_settings()
