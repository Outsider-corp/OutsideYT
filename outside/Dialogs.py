import glob
import os
from functools import partial

from outside import TableModels, YT_Uploader
from PyQt5 import QtWidgets, QtGui, QtCore
import OutsideYT
from outside.views_py import UsersList_Dialog, AddAccount_Dialog, SelectVideos_Dialog, UpdateTime_Dialog, \
    UploadTime_for_Video_Dialog


def open_UsersList_Dialog(parent):
    cookies_dir = os.path.join(os.path.dirname(OutsideYT.app_settings_uploaders.file), "uploaders")
    dialog, dialog_settings = userslist(parent)
    dialog.setWindowTitle("Uploaders List")
    dialog_model = TableModels.UsersModel()
    dialog_settings.Users_Table.setModel(dialog_model)
    dialog_settings.Users_Table.setItemDelegate(TableModels.InLineEditDelegate())
    dialog_settings.Users_Table = TableModels.table_universal(dialog_settings.Users_Table)
    width = dialog.width() - 30
    dialog_settings.Users_Table.setColumnWidth(0, int(width * 0.1))
    dialog_settings.Users_Table.setColumnWidth(1, int(width * 0.3))
    dialog_settings.Users_Table.setColumnWidth(2, width - int(width * 0.1) - int(width * 0.3))
    dialog_settings.Users_Table.horizontalHeader().setFont(QtGui.QFont("Arial", 14))
    dialog_settings.DefUser_ComboBox = update_combobox(dialog_settings.DefUser_ComboBox,
                                                       ["No default account",
                                                        *OutsideYT.app_settings_uploaders.accounts.keys()])
    adduser = partial(open_addUser_Dialog, parent=dialog, parent_settings=dialog_settings)
    dialog_settings.addUser_Button.clicked.connect(adduser)
    dialog_settings.primary_state = [dialog_settings.DefUser_ComboBox.currentText(),
                                     dialog_settings.Users_Table.model().get_data().copy()]

    def chk_cookies():
        files = glob.glob(f'{cookies_dir}/*_cookies')
        cook = QtWidgets.QDialog(dialog)
        cook.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        cook_settings = AddAccount_Dialog.Ui_AddUser_Dialog()
        cook_settings.setupUi(cook)
        cook_settings.Account_textbox.setEnabled(False)
        for file in files:
            filename = os.path.basename(file).replace("_cookies", "")
            if filename in list(OutsideYT.app_settings_uploaders.accounts.keys()):
                continue
            cook_settings.Account_textbox.setText(filename)

            def ok():
                OutsideYT.app_settings_uploaders.add_account({
                    filename: cook_settings.Gmail_textbox.text()})

            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(cook.reject)
            cook_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)
            cook.exec_()
        dialog_settings.Users_Table.model().update()
        dialog_settings.DefUser_ComboBox = update_combobox(dialog_settings.DefUser_ComboBox,
                                                           ["No default account",
                                                            *OutsideYT.app_settings_uploaders.accounts.keys()])

    dialog_settings.CheckCookies_Button.clicked.connect(chk_cookies)

    def cancel():
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != dialog_settings.DefUser_ComboBox.currentText()) or \
                not (dialog_settings.primary_state[1].equals(dialog_settings.Users_Table.model().get_data().copy())):
            confirm = QtWidgets.QMessageBox()
            confirm.setText(f"Are you sure you want to cancel?\n"
                            f"All changes will be lost!")
            confirm.setWindowTitle("Confirmation")
            confirm.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm.setDefaultButton(QtWidgets.QMessageBox.No)
            result = confirm.exec_()
            if result == QtWidgets.QMessageBox.Yes:
                confirm.reject()
                dialog.reject()
        else:
            dialog.reject()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(cancel)

    def save():
        if ([dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Users_Table.model().rowCount())]
            != list(dialog_settings.primary_state[1].index)) or \
                (dialog_settings.primary_state[0] != dialog_settings.DefUser_ComboBox.currentText()) or \
                not (dialog_settings.primary_state[1].equals(dialog_settings.Users_Table.model().get_data().copy())):
            def_user = dialog_settings.DefUser_ComboBox.currentText()
            if def_user == "No default account":
                def_user = ""
            if def_user != OutsideYT.app_settings_uploaders.def_account:
                OutsideYT.app_settings_uploaders.add_def_account(def_user)
            for ind, file in dialog_settings.primary_state[1].iterrows():
                old = file.Account
                new = dialog_settings.Users_Table.model().get_data().loc[ind, "Account"]
                if old != new:
                    os.rename(os.path.join(cookies_dir, f'{old}_cookies'), os.path.join(cookies_dir, f'{new}_cookies'))
                    if old == OutsideYT.app_settings_uploaders.def_account:
                        OutsideYT.app_settings_uploaders.add_def_account(new)
            dialog_settings.Users_Table.model().reset_ids(
                [dialog_settings.Users_Table.verticalHeader().visualIndex(i) for i in
                 range(dialog_settings.Users_Table.model().rowCount())])
            dialog_settings.Users_Table.model()._data = dialog_settings.Users_Table.model().get_data().sort_values(
                by="id")
            accs = dialog_settings.Users_Table.model().get_data().set_index("Account")["Gmail"].to_dict()
            OutsideYT.app_settings_uploaders.update_accounts(accs)

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)
    dialog.exec_()


def open_Watchers_List_Dialog(parent):
    dialog, dialog_settings = userslist(parent)
    dialog.setWindowTitle("Watchers List")
    dialog.exec_()


def open_addUser_Dialog(parent: QtWidgets.QTableView, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = AddAccount_Dialog.Ui_AddUser_Dialog()
    dialog_settings.setupUi(dialog)

    def ok():
        login = dialog_settings.Account_textbox.text()
        mail = dialog_settings.Gmail_textbox.text()
        if login in list(OutsideYT.app_settings_uploaders.accounts.keys()):
            TableModels.error_func("This account name is already used!")
        else:
            try:
                dialog.close()
                added = YT_Uploader.google_login(login, mail)
                if added:
                    OutsideYT.app_settings_uploaders.add_account({login: mail})
                    parent_settings.primary_state[1] = parent_settings.Users_Table.model().get_data().copy()
                    parent_settings.Users_Table.model().update()
                    parent_settings.DefUser_ComboBox = update_combobox(parent_settings.DefUser_ComboBox,
                                                                       ["No default account",
                                                                        *OutsideYT.app_settings_uploaders.accounts.keys()])
            except:
                TableModels.error_func("Error.")

    dialog.accept = ok
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog.exec_()

class SetPublishTimeDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, table=None):
        self.table = table
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        if event.type() in [event.MouseButtonDblClick, event.MouseButtonDblClick, event.MouseButtonDblClick,
                            event.MouseButtonDblClick]:
            set_upload_time_for_video(self.parent(), self.table, index.row())
        return super().editorEvent(event, model, option, index)

def open_upload_select_videos(parent, table):
    dialog = QtWidgets.QDialog(parent)
    dialog_settings = SelectVideos_Dialog.Ui_SelectVideos_Dialog()
    dialog_settings.setupUi(dialog)
    dialog_settings.Users_ComboBox = update_combobox(dialog_settings.Users_ComboBox,
                                                     ["No default account",
                                                      *OutsideYT.app_settings_uploaders.accounts.keys()])

    def select_video(next_func):
        try:
            path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Video", ".",
                                                              QtWidgets.QFileDialog.ShowDirsOnly)
            print(path)
            next_func(path=path)
            dialog.accept()
        except Exception as e:
            if path == "":
                return
            TableModels.error_func(f"Error.\n {e}")

    def del_vids_folder():
        try:
            OutsideYT.app_settings_uploaders.del_vids_folder()
            dialog.accept()
        except Exception as e:
            TableModels.error_func(f"Error.\n {e}")

    def select_folder(path):
        user = dialog_settings.Users_ComboBox.currentText()
        if user == "No default account":
            user = ""
        for smth in os.scandir(path):
            if smth.is_dir():
                TableModels.add_video_for_uploading(table, os.path.abspath(smth), user=user)

    dialog_settings.SelectVideo_Button.clicked.connect(
        partial(select_video, partial(TableModels.add_video_for_uploading, table=table)))
    dialog_settings.SelectFolderForUser_Button.clicked.connect(partial(select_video, select_folder))
    dialog_settings.ChangeDefFolder_Button.clicked.connect(partial(select_video, change_def_folder))
    dialog_settings.SetDefFolder_Button.clicked.connect(del_vids_folder)
    dialog.exec_()


def scan_videos_folder(table):
    users = list(OutsideYT.app_settings_uploaders.accounts.keys())
    for user in users:
        for vid in os.scandir(os.path.join(OutsideYT.app_settings_uploaders.vids_folder, user)):
            if vid.is_dir():
                TableModels.add_video_for_uploading(table, os.path.abspath(vid), user)


def update_combobox(combobox, items):
    combobox.clear()
    combobox.addItems(items)
    if OutsideYT.app_settings_uploaders.def_account != "":
        combobox.setCurrentIndex(list(OutsideYT.app_settings_uploaders.accounts.keys()).index(
            OutsideYT.app_settings_uploaders.def_account) + 1)
    else:
        combobox.setCurrentIndex(0)
    return combobox


def change_def_folder(path):
    if path == "":
        return
    if os.path.isdir(path):
        OutsideYT.app_settings_uploaders.add_vids_folder(path)
    else:
        TableModels.error_func("This is not a directory!")


def google_login(login, mail, parent: QtWidgets.QDialog):
    if login in list(OutsideYT.app_settings_uploaders.accounts.keys()):
        TableModels.error_func("This account name is already used!")
    else:
        try:
            YT_Uploader.google_login(login, mail)
            parent.parent().update()
        except:
            TableModels.error_func("Error.")


def userslist(parent):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = UsersList_Dialog.Ui_UsersList_Dialog()
    dialog_settings.setupUi(dialog)
    return dialog, dialog_settings


def set_upload_time(parent, table: QtWidgets.QTableView):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = UpdateTime_Dialog.Ui_Upload_Time()
    dialog_settings.setupUi(dialog)
    dialog_settings.User_ComboBox_1 = update_combobox(dialog_settings.User_ComboBox_1,
                                                      ["All accounts",
                                                       *OutsideYT.app_settings_uploaders.accounts.keys()])
    dialog_settings.User_ComboBox_1.setCurrentIndex(0)
    dialog_settings.startTimeEdit_1.setDateTime(
        QtCore.QDateTime(QtCore.QDate.currentDate().addDays(1), QtCore.QTime(0, 0, 0)))
    dialog_settings.startTimeEdit_1.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate.currentDate(),
                                                                        QtCore.QTime.currentTime().addSecs(60 * 60)))
    lines_visible = [dialog_settings.label_User, dialog_settings.User_ComboBox_1]

    def add_line():
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        row = dialog_settings.gridLayout.rowCount()
        if row > 8:
            TableModels.error_func("Too many loops!")
            return
        start = QtWidgets.QDateTimeEdit(dialog)
        start.setFont(font)
        start.setCalendarPopup(True)
        start.setObjectName(f"startTimeEdit_{row}")
        start.setDateTime(QtCore.QDateTime(QtCore.QDate.currentDate().addDays(1), QtCore.QTime(0, 0, 0)))
        start.setMinimumDateTime(
            QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime().addSecs(60 * 60)))
        dialog_settings.gridLayout.addWidget(start, row, 0, 1, 1)
        setattr(dialog_settings, f"startTimeEdit_{row}", start)

        time_layout = QtWidgets.QHBoxLayout()
        time_layout.setObjectName(f"time_layout_{row}")

        days_Spin = QtWidgets.QSpinBox(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(days_Spin.sizePolicy().hasHeightForWidth())
        days_Spin.setSizePolicy(sizePolicy)
        days_Spin.setFont(font)
        days_Spin.setObjectName(f"days_Spin_{row}")
        time_layout.addWidget(days_Spin)
        setattr(dialog_settings, f"days_Spin_{row}", days_Spin)

        timeEdit = QtWidgets.QTimeEdit(dialog)
        timeEdit.setFont(font)
        timeEdit.setObjectName(f"timeEdit_{row}")
        time_layout.addWidget(timeEdit)
        dialog_settings.gridLayout.addLayout(time_layout, row, 1, 1, 1)
        setattr(dialog_settings, f"timeEdit_{row}", timeEdit)

        combo = QtWidgets.QComboBox(dialog)
        combo.setFont(font)
        combo.setObjectName(f"User_ComboBox_{row}")
        combo = update_combobox(combo, ["All accounts", *OutsideYT.app_settings_uploaders.accounts.keys()])
        combo.setCurrentIndex(0)
        dialog_settings.gridLayout.addWidget(combo, row, 2, 1, 1)
        setattr(dialog_settings, f"User_ComboBox_{row}", combo)
        lines_visible.append(combo)

        video_spin = QtWidgets.QSpinBox(dialog)
        video_spin.setFont(font)
        video_spin.setObjectName(f"videoCount_Spin_{row}")
        dialog_settings.gridLayout.addWidget(video_spin, row, 3, 1, 1)
        setattr(dialog_settings, f"videoCount_Spin_{row}", video_spin)

    dialog_settings.AddLoop_Button.clicked.connect(add_line)

    def change_radio(chk):
        for el in lines_visible:
            el.setVisible(chk)

    dialog_settings.Loop_radio.toggled.connect(lambda: change_radio(True))
    dialog_settings.LoopGlobal_radio.toggled.connect(lambda: change_radio(False))

    def ok():
        if dialog_settings.Loop_radio.isChecked():
            for row in range(1, dialog_settings.gridLayout.rowCount()):
                data = table.model().get_data()
                user = getattr(dialog_settings, f"User_ComboBox_{row}").currentText()
                if user == "All accounts":
                    user_lines = data[(data.Publish == "Now") | (data.Publish == "")].reset_index(drop=True)
                else:
                    user_lines = data[data.User == user][(data.Publish == "Now") | (data.Publish == "")].reset_index(
                        drop=True)
                if len(user_lines) == 0:
                    continue
                time = getattr(dialog_settings, f"timeEdit_{row}").time()
                days = getattr(dialog_settings, f"days_Spin_{row}").value()
                upload_time = getattr(dialog_settings, f"startTimeEdit_{row}").dateTime()
                vids_count = getattr(dialog_settings, f"videoCount_Spin_{row}").value()
                if vids_count == 0:
                    vids_count = len(user_lines)
                vids_count = min(vids_count, len(user_lines))
                for i in range(vids_count):
                    table.model().setData(
                        table.model().index(user_lines.at[i, "id"] - 1, list(user_lines.columns).index("Publish"),
                                            QtCore.QModelIndex()), upload_time.toString("dd.MM.yyyy hh:mm"),
                        role=QtCore.Qt.DisplayRole)
                    upload_time = upload_time.addDays(days)
                    upload_time = upload_time.addSecs(time.hour() * 3600 + time.minute() * 60 + time.second())
        else:
            pass
        table.update()
        dialog.accept()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)
    dialog.exec_()


def set_upload_time_for_video(parent, table, video_id):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = UploadTime_for_Video_Dialog.Ui_Upload_Time_for_video()
    dialog_settings.setupUi(dialog)
    dialog_settings.Video_label.setText(table.model().get_data().at[video_id, 'Title'])
    dialog_settings.Day.setDateTime(QtCore.QDateTime(QtCore.QDate.currentDate().addDays(1), QtCore.QTime(0, 0, 0)))
    dialog_settings.Day.setMinimumDateTime(
        QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime().addSecs(60 * 60)))

    def ok():
        time = dialog_settings.Time.text()
        if len(time.split(":")[0]) == 1:
            time = "0" + time
        date = " ".join([dialog_settings.Day.text(), time])
        table.model()._data.at[video_id, "Publish"] = date
        table.update()
        dialog.accept()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)
    dialog.exec_()

def clear_upload_time(parent, table: QtWidgets.QTableView):
    message_box = QtWidgets.QMessageBox(parent)
    message_box.setIcon(QtWidgets.QMessageBox.Question)
    message_box.setWindowTitle("Confirmation")
    message_box.setText("Are you sure?\nAll upload times will be deleted!")
    message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    message_box.setDefaultButton(QtWidgets.QMessageBox.No)
    res = message_box.exec_()
    if res == QtWidgets.QMessageBox.Yes:
        table.model()._data["Publish"] = "Now"
        table.update()