import glob
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore

import OutsideYT
import outside.Watch.TableModels
import outside.Watch.context_menu
from outside.YT_functions import get_video_info, get_playlist_info, select_page
from outside.asinc_functions import start_operation
from outside.message_boxes import warning_func, error_func
from outside.functions import update_combobox
from outside.views_py import EditWatchersGroups_Dialog, SelectWatchVideos_Dialog


def edit_watchers_groups(parent, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = EditWatchersGroups_Dialog.Ui_GroupsList_Dialog()
    dialog_settings.setupUi(dialog)
    dialog_model = outside.Watch.TableModels.WatchersGroupsModel()
    dialog_settings.Groups_Table.setModel(dialog_model)
    dialog_settings.Groups_Table.horizontalHeader().setFont(QtGui.QFont("Arial", 14))
    width = dialog.width() - 30
    dialog_settings.Groups_Table.setColumnWidth(0, int(width * 0.1))
    dialog_settings.Groups_Table.setColumnWidth(1, int(width * 0.45))
    dialog_settings.Groups_Table.setColumnWidth(2, width - int(width * 0.55))
    dialog_settings.primary_state = dialog_settings.Groups_Table.model().get_data().copy()
    dialog_settings.Groups_Table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    dialog_settings.Groups_Table.customContextMenuRequested.connect(
        lambda pos: outside.Watch.context_menu.watchers_group_dialogs_menu(pos, parent=dialog,
                                                                           table=dialog_settings.Groups_Table))

    def cancel():
        if ([dialog_settings.Groups_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Groups_Table.model().rowCount())]
            != list(dialog_settings.primary_state.index)) or \
                not (dialog_settings.primary_state.equals(dialog_settings.Groups_Table.model().get_data().copy())):
            if warning_func(parent=parent, text=f"Are you sure you want to cancel?\n"
                                                f"All changes will be lost!"):
                dialog.reject()
        else:
            dialog.reject()

    def add_group():
        dialog_settings.Groups_Table.model().insertRows()
        dialog_settings.Groups_Table.update()

    dialog_settings.addGroup_Button.clicked.connect(add_group)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(partial(cancel))

    def save():
        new_data = dialog_settings.Groups_Table.model().get_data()
        if not new_data["New Group name"].isna().all():
            for ind, row in new_data.iterrows():
                if row.Group != row["New Group name"] and row["New Group name"]:
                    OutsideYT.app_settings_watchers.change_group_name(row.Group, row["New Group name"])
        dialog_settings.Groups_Table.model().reset_ids(
            [dialog_settings.Groups_Table.verticalHeader().visualIndex(i) for i in
             range(dialog_settings.Groups_Table.model().rowCount())])
        dialog_settings.Groups_Table.model()._data = dialog_settings.Groups_Table.model().get_data().sort_values(
            by="id")
        parent_settings.Users_Table.model().update()
        items = list(OutsideYT.app_settings_watchers.groups.keys())
        parent_settings.Group_comboBox = update_combobox(
            parent_settings.Group_comboBox, items, OutsideYT.app_settings_watchers.def_group)
        dialog.accept()

    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(save)
    dialog.exec_()


def open_watch_select_videos(parent, table: QtWidgets.QTableView, parent_settings):
    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    dialog_settings = SelectWatchVideos_Dialog.Ui_SelectVideos_Dialog()
    dialog_settings.setupUi(dialog)

    radios = [dialog_settings.Last_video_radioButton, dialog_settings.Random_video_radioButton,
              dialog_settings.Period_radioButton]
    var1 = [dialog_settings.Count_label, dialog_settings.Count_videos_spinBox]
    var2 = [dialog_settings.Start_label, dialog_settings.Start_date, dialog_settings.End_label,
            dialog_settings.End_date]

    def add_video():
        text = select_page("video")
        if text:
            group = dialog_settings.Group_comboBox.currentText()
            add_video_to_table(table, text, group)
            dialog.accept()
        else:
            error_func("Not valid link.", dialog)

    def add_playlist():
        error_func("This action will be add later...")
        return
        # text = select_page("playlist")
        # if text:
        #     group = dialog_settings.Group_comboBox.currentText()
        #     add_video_to_table(table, text, group)
        #     dialog.accept()
        # else:
        #     error_func("Not valid link.", dialog)

    def import_links_from_file():
        """
        It's generator that give count of steps on first yeild
        """
        file = ""
        try:
            exts = OutsideYT.text_extensions
            file, _ = QtWidgets.QFileDialog.getOpenFileName(None, f"Select File with Links", "",
                                                            f"Text Files ({' '.join('*' + ex for ex in exts)})")
            group = dialog_settings.Group_comboBox.currentText()
            dialog.accept()
            with open(file, "r", encoding="UTF-8") as f:
                links = f.readlines()
            yield len(links)
            for num, link in enumerate(links):
                add_video_to_table(table=table, link=link, group=group)
                yield num + 1
        except Exception as e:
            if file == "":
                return
            error_func(f"Error.\n {e}")

    def select_channel():
        text = select_page("channel")
        if text:
            dialog_settings.channel_link_textBox.setText(text)
        else:
            error_func("Not valid link.", dialog)

    def show_elements(group):
        """
        Args:
            group: str - "none" - hide all elements, "count" - show count elements and radios,
            "period" - show period elements and radios
        """
        if group == "none":
            for el in radios + var1 + var2:
                el.setVisible(False)
        elif group == "count":
            for el in radios + var1:
                el.setVisible(True)
            for el in var2:
                el.setVisible(False)
        elif group == "period":
            for el in radios + var2:
                el.setVisible(True)
            for el in var1:
                el.setVisible(False)

    def show_actions_for_channel():
        if dialog_settings.channel_link_textBox.text() == "":
            show_elements("none")
        else:
            show_elements("count")

    def ok():
        url = dialog_settings.channel_link_textBox.text()
        if url == "":
            dialog.reject()
        elif "youtube.com/" not in url:
            error_func(f"Wrong url: {url}")
        else:
            group = dialog_settings.Group_comboBox.currentText()
            if dialog_settings.Last_video_radioButton.isChecked():
                count = dialog_settings.Count_videos_spinBox.value()

                # table.model().insertRows(row_content={"Watchers Group": group,
                #                                       "Video": video,
                #                                       "Channel": channel,
                #                                       "Link": link})

            elif dialog_settings.Random_video_radioButton.isChecked():
                count = dialog_settings.Count_videos_spinBox.value()
            else:
                start = dialog_settings.Start_date.time()
                end = dialog_settings.End_date.time()

    items = list(OutsideYT.app_settings_watchers.groups.keys())
    dialog_settings.Group_comboBox = update_combobox(
        dialog_settings.Group_comboBox, items, OutsideYT.app_settings_watchers.def_group)

    show_elements("none")
    dialog_settings.channel_link_textBox.textChanged.connect(show_actions_for_channel)
    dialog_settings.Last_video_radioButton.toggled.connect(lambda: show_elements("count"))
    dialog_settings.Random_video_radioButton.toggled.connect(lambda: show_elements("count"))
    dialog_settings.Period_radioButton.toggled.connect(lambda: show_elements("period"))

    dialog_settings.AddVideo_Button.clicked.connect(add_video)
    dialog_settings.AddPlaylist_Button.clicked.connect(add_playlist)
    dialog_settings.Import_links_Button.clicked.connect(partial(start_operation,
                                                                dialog=parent,
                                                                dialog_settings=parent_settings,
                                                                page="WatchPage",
                                                                progress_bar=parent_settings.Watch_Progress_Bar,
                                                                process=import_links_from_file))
    dialog_settings.Select_channel_Button.clicked.connect(select_channel)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog_settings.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)

    dialog.exec_()


def open_advanced_settings(parent, table):
    error_func("This action will be add later...")


def add_video_to_table(table, link: str = "", group=None, textbox: QtWidgets.QLineEdit = None):
    if group is None:
        group = OutsideYT.app_settings_watchers.def_group
    if not link:
        if not textbox:
            return
        link = textbox.text()
    if "youtube.com/watch" in link or 'youtu.be/' in link:
        video, channel, duration = get_video_info(link)
        if video and channel and duration:
            table.model().insertRows(row_content={"Watchers Group": group,
                                                  "Video": video,
                                                  "Channel": channel,
                                                  "Duration": duration,
                                                  "Link": link})
    elif "youtube.com/playlist" in link:
        videos = get_playlist_info(link)
        if videos:
            for video, channel, video_link in videos:
                table.model().insertRows(row_content={"Watchers Group": group,
                                                      "Video": video,
                                                      "Channel": channel,
                                                      "Link": video_link})
    else:
        return
    if textbox is not None:
        textbox.clear()
        table.update()
