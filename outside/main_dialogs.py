import glob
import os
from functools import partial
from typing import List, Any

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableView, QWidget

import outside.Watch.context_menu as watch_context
from outside.OYT_Settings import app_settings_uploaders, app_settings_watchers, TEXT_EXTENSIONS, \
    app_settings_download
import outside.context_menu
from outside import TableModels
from outside.asinc_functions import GetVideoInfoThread, CheckCookiesLifeThread
from outside.functions import update_combobox, get_video_id, change_enabled_tab_elements
from outside.message_boxes import error_func, warning_func, choose_func, info_func
from outside.Upload.dialogs import google_login, update_uploads_delegate
from outside.views_py import (
    AddUser_Dialog,
    AddWatcher_Dialog,
    UsersList_Dialog,
    WatchersList_Dialog,
)
from outside.Watch.dialogs import edit_watchers_groups
from outside.YT.functions import get_playlist_info, select_page


def open_UsersList_Dialog(parent, table_type: str, add_table_class, parent_settings):
    if table_type in ['upload', 'download']:
        table_settings = app_settings_uploaders
        def_type = 'account'
        combo_items_default = table_settings.accounts.keys()
    elif table_type == 'watch':
        table_settings = app_settings_watchers
        def_type = 'group'
        combo_items_default = table_settings.groups.keys()
    else:
        return
    table_settings.update_settings()
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
    if table_type in ['upload', 'download']:
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
                      dialog_ui=AddUser_Dialog.Ui_AddUser_Dialog if table_type in ['upload',
                                                                                   'download']
                      else AddWatcher_Dialog.Ui_AddUser_Dialog)
    dialog_settings.addUser_Button.clicked.connect(adduser)
    dialog_settings.Users_Table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def context_menu(pos):
        if table_type in ['upload', 'download']:
            outside.context_menu.users_dialogs_menu(pos, parent=dialog,
                                                    table=dialog_settings.Users_Table,
                                                    table_type=table_type)
        elif table_type == 'watch':
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
                    if table_type in ['upload', 'download']:
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
            if table_type in ['upload', 'download']:
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
            if table_type != 'watch':
                parent_settings.Download_Save_to_ComboBox = update_combobox(
                    parent_settings.Download_Save_to_ComboBox,
                    table_settings.accounts.keys(),
                    table_settings.def_account if table_settings.def_account != f'No default {def_type}'
                    else ''
                )
                update_uploads_delegate(parent_settings.Upload_Table)

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)

    def chk_cookies():
        def ok(filename, cook_settings):
            if hasattr(cook_settings, 'Group_comboBox'):
                table_settings.add_account(
                    group=cook_settings.Group_comboBox.currentText(),
                    acc={filename: cook_settings.Gmail_textbox.text()})
            else:
                table_settings.add_account(
                    {filename: cook_settings.Gmail_textbox.text()})

        files = glob.glob(f'{table_settings.cookies_folder}/*_cookies')
        all_accounts = table_settings.accounts
        for file in files:
            filename = os.path.basename(file).replace('_cookies', '')
            if filename in all_accounts:
                continue

            cook = QtWidgets.QDialog(dialog)
            cook.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
            if table_type in ['upload', 'download']:
                cook_settings = AddUser_Dialog.Ui_AddUser_Dialog()
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
        open_UsersList_Dialog(parent, table_type, add_table_class, parent_settings)

    dialog_settings.CheckCookies_Button.clicked.connect(chk_cookies)

    def chk_cookies_life():
        def change_enabled_elements(state: bool):
            for el in dialog.findChildren(QWidget):
                el.setEnabled(state)

        def finish(thread):
            try:
                if thread.to_delete:
                    accs = {acc: table_settings.accounts[acc] for acc in thread.to_delete}
                    accs_list = [f'  {acc} ({gmail}@gmail.com)' for acc, gmail in accs.items()]
                    ans = choose_func(
                        text=f'Do you want to delete dead cookies or log in again?\n\n' + '\n'.join(
                            accs_list),
                        vars={'Delete dead cookies': 0, 'Relogin dead cookies': 1},
                        standart_var='Delete dead cookies')
                    if ans != -1:
                        for acc in thread.to_delete:
                            group_val = table_settings.find_group(
                                acc) if table_type == 'watch' else None
                            table_settings.del_account(acc, confirm=True)
                            if ans == 1:
                                open_addUsers_Dialog(parent=dialog,
                                                     parent_settings=dialog_settings,
                                                     table_settings=table_settings,
                                                     def_type=def_type,
                                                     combo_items_default=combo_items_default,
                                                     dialog_ui=AddUser_Dialog
                                                     .Ui_AddUser_Dialog if table_type in [
                                                         'upload',
                                                         'download']
                                                     else AddWatcher_Dialog.Ui_AddUser_Dialog,
                                                     account_val=acc,
                                                     gmail_val=accs[acc],
                                                     group_val=group_val)
                        dialog.close()
                        open_UsersList_Dialog(parent, table_type, add_table_class, parent_settings)
                else:
                    info_func('All cookies are alive!')
            except KeyError as e:
                error_func(f'No account {e} in settings file')
            change_enabled_elements(True)

        if not table_settings.accounts:
            info_func("You don't have any accounts.")
            return
        change_enabled_elements(False)
        chk_thread = CheckCookiesLifeThread(table_settings)
        chk_thread.finished.connect(partial(finish, thread=chk_thread))
        chk_thread.start()

    dialog_settings.ALive_Cookies_Button.clicked.connect(chk_cookies_life)

    if table_type == 'watch':
        dialog_settings.EditGroups_Button.clicked.connect(
            partial(edit_watchers_groups, parent=dialog, parent_settings=dialog_settings))
        dialog_settings.Users_Table.model().update()
        dialog.parent().update()
    dialog.exec_()


def open_addUsers_Dialog(parent, parent_settings, table_settings,
                         def_type: str, dialog_ui, combo_items_default: list,
                         account_val=None,
                         gmail_val=None,
                         group_val=None):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    dialog_settings = dialog_ui()
    dialog_settings.setupUi(dialog)
    items = [f'No {def_type}', *combo_items_default]
    dialog_settings = update_settings_combobox_with_type(dialog_settings, items,
                                                         table_type=str(table_settings).lower())
    if hasattr(dialog_settings, 'Group_comboBox') and group_val:
        index = list(items).index(group_val)
        dialog_settings.Group_comboBox.setCurrentIndex(index)
    dialog_settings.Account_textbox.setText(account_val)
    dialog_settings.Gmail_textbox.setText(gmail_val)

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
                        items=items, table_type=str(table_settings))
            except Exception as e:
                error_func(f'Error. \n{e}')

    dialog.accept = partial(ok, parent_settings=parent_settings)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(
        dialog.reject)
    dialog.exec_()


def open_watch_down_select_videos(parent, table: QtWidgets.QTableView, parent_settings,
                                  add_table_class):
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
            group = dialog_settings.Group_comboBox.currentText() if \
                table.model().table_type == 'watch' else None
            get_videos_info(table, links=[text], group=group, dialog_settings=parent_settings,
                            add_args=['cards',
                                      'streamingData'] if (
                                    table.model().table_type == 'download') else None)
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
        try:
            exts = TEXT_EXTENSIONS
            file, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                                            f'Select File with Links', '',
                                                            f"Text Files ("
                                                            f"{' '.join('*' + ex for ex in exts)})")
            if not file:
                return

            group = dialog_settings.Group_comboBox.currentText() if \
                table.model().table_type == 'watch' else None
            dialog.accept()

            with open(file, 'r', encoding='UTF-8') as f:
                links = f.readlines()
            add_args = ['cards',
                        'streamingData'] if table.model().table_type == 'download' else None
            get_videos_info(table=table, links=links, group=group, add_args=add_args,
                            dialog_settings=parent_settings)
        except Exception as e:
            print(f'Error on importing links...\n{e}')

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

    def ok():
        url = dialog_settings.channel_link_textBox.text()
        if not url:
            dialog.reject()
        elif 'youtube.com/' not in url:
            error_func(f'Wrong url: {url}')
        else:
            if table.model().table_type == 'watch':
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

    if table.model().table_type == 'watch':
        items = list(app_settings_watchers.groups.keys())
        dialog_settings.Group_comboBox = update_combobox(
            dialog_settings.Group_comboBox, items, app_settings_watchers.def_group)

    show_elements('count')

    dialog_settings.Last_video_radioButton.toggled.connect(lambda: show_elements('count'))
    dialog_settings.Random_video_radioButton.toggled.connect(lambda: show_elements('count'))
    dialog_settings.Period_radioButton.toggled.connect(lambda: show_elements('period'))

    dialog_settings.AddVideo_Button.clicked.connect(add_video)
    dialog_settings.AddPlaylist_Button.clicked.connect(add_playlist)
    dialog_settings.Import_links_Button.clicked.connect(import_links_from_file)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(
        dialog.reject)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)

    dialog.exec_()


def add_video_from_textbox(table, textbox: QtWidgets.QLineEdit, dialog_settings):
    text = textbox.text()
    if 'youtube.com/watch' in text or 'youtu.be/' in text:
        get_videos_info(table, [text], dialog_settings,
                        add_args=['cards',
                                  'streamingData'] if (
                                    table.model().table_type == 'download') else None)
        textbox.clear()
    elif 'youtube.com/playlist' in text:
        get_playlist_info(table, text)
        textbox.clear()


def get_videos_info(table, links: List, dialog_settings, group=None, add_args=None):
    def return_func(thread):
        try:
            results = thread.results
            thread.quit()
            if thread.wait():
                for video in results:
                    _add_video_to_table(table, video_info=video, group=group)
            thread.terminate()
        except Exception as e:
            print(f'Error on add video info to table...\n{e}')
        finally:
            change_enabled_tab_elements(dialog_settings=dialog_settings,
                                        page_name=table.model().table_type.capitalize(),
                                        state=True)

    try:
        change_enabled_tab_elements(dialog_settings=dialog_settings,
                                    page_name=table.model().table_type.capitalize(),
                                    state=False, block_start_button=True)
        links_add = [link for link in links if
                     link not in table.model().get_data()['Link'].to_list()]
        table.model().progress_label.setText('Get info about videos...')
        vids_thread = GetVideoInfoThread(tasks=links_add, progress_bar=table.model().progress_bar,
                                         progress_label=table.model().progress_label,
                                         additional_args=add_args)
        vids_thread.finished.connect(partial(return_func, vids_thread))
        vids_thread.update_progress_signal.connect(lambda x: update_progress_bar(table, x))
        vids_thread.update_progress_label_signal.connect(lambda x: update_progress_label(table, x))
        vids_thread.start()

    except Exception as e:
        print(f'Error on get video info...\n{e}')


def get_playlist_info(table, link: str, group: str = None):
    pass


def _add_video_to_table(table, video_info, group=None, force_add=False):
    if video_info:
        try:
            link = get_video_id(video_info['link'])
            if not force_add and link in table.model().get_data()['Link'].to_list():
                print(f'{video_info["title"]} is already added.')
                return
            row_content = {'Watchers Group': group,
                           'Video': video_info['title'],
                           'Channel': video_info['author'],
                           'Duration': video_info['lengthSeconds'],
                           'Link': link,
                           '_download_info': video_info}
            table.model().insertRows(row_content=row_content)
        except KeyError:
            pass


def userslist(parent, table_name: str):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    if table_name in ['upload', 'download']:
        dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    else:
        dialog_settings = WatchersList_Dialog.Ui_WatchersList_Dialog()
    dialog_settings.setupUi(dialog)
    return dialog, dialog_settings


def update_settings_combobox_with_type(dialog_settings, items, table_type):
    if table_type == 'watch':
        dialog_settings.Group_comboBox = update_combobox(
            dialog_settings.Group_comboBox, items[1:], app_settings_watchers.def_group)
    elif hasattr(dialog_settings, 'DefUser_CompBox'):
        if table_type == 'upload':
            dialog_settings.DefUser_ComboBox = update_combobox(
                dialog_settings.DefUser_ComboBox, items,
                app_settings_uploaders.def_account)
    return dialog_settings


def update_settings_from_file():
    app_settings_uploaders.update_settings()
    app_settings_watchers.update_settings()
    app_settings_download.update_settings()


def update_progress_bar(table: QTableView, value: int):
    if table.model().progress_bar:
        table.model().progress_bar.setValue(value)


def update_progress_label(table: QTableView, label_text: str):
    if table.model().progress_label:
        table.model().progress_label.setText(label_text)


def add_progress_label(table: QTableView, add_key: bool = False, add_text: str = ''):
    add_key, add_text = yield
    label = table.model().progress_label
    if label:
        old_text = label.text()
        while True:
            if add_key:
                label.setText(f'{old_text} / {add_text}')
                add_key, add_text = yield
            else:
                label.setText(old_text)
                break
    return


def cancel_page_action(dialog_settings, table: QTableView):
    table_type = table.model().table_type
    if getattr(dialog_settings, f'{table_type.lower()}_thread'):
        getattr(dialog_settings, f'{table_type.lower()}_thread').stop_signal = True


def init_add_label_generator(table):
    add_label_gen = add_progress_label(table, True, '')
    next(add_label_gen)
    return add_label_gen
