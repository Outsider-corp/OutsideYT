import typing

import pandas as pd
from PyQt5.QtCore import QModelIndex, QAbstractTableModel, Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QTableView, QFileDialog

from OutsideYT import app_settings_uploaders, video_extensions, image_extensions, text_extensions
from outside.functions import find_files
from outside.message_boxes import error_func


class UploadModel(QAbstractTableModel):
    columns = ["id", "Selected", "User", "Title", "Publish", "Video", "Description",
               "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
               "Save filename?"]

    default_content = {"id": None, "Selected": True,
                       "User": app_settings_uploaders.def_account,
                       "Title": "", "Publish": "Now", "Video": "select video",
                       "Description": "", "Playlist": "", "Preview": "",
                       "Tags": "", "Ends": "random", "Cards": 2,
                       "Access": "Private", "Save filename?": False}

    def __init__(self, data=None, oldest_settings=None):
        QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=UploadModel.columns)
        self._data = data
        self.paths = []
        self.oldest_settings = oldest_settings

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] == "id" or self._data.columns[index.column()] == "Save filename?":
            flags = Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        elif self._data.columns[index.column()] in ["Publish", "Video", "Preview"]:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return flags

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and self._data.columns[section] != "Selected":
                return self._data.columns[section]
            elif orientation == Qt.Vertical:
                return ">"

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.CheckStateRole:
                if column == "id":
                    return Qt.Checked if self._data.loc[index.row(), "Selected"] else Qt.Unchecked
                elif column == "Save filename?":
                    if self.get_data().loc[index.row(), "Title"] == "":
                        return Qt.Checked if self.get_data().loc[
                            index.row(), "Save filename?"] else Qt.Unchecked
            if role == Qt.DisplayRole:
                if column == "Selected" or column == "Save filename?":
                    return
                if column == "Publish":
                    return self.get_data().loc[index.row(), column]

                elif column == "Video":
                    v = self.get_data().loc[index.row(), column]
                    return self.get_data().loc[index.row(), column].split("/")[-1] \
                        if len(v.split("/")) > 1 else v

                elif column == "Description":
                    return self.get_data().loc[index.row(), column]

                elif column == "Playlist":
                    return self.get_data().loc[index.row(), column]

                elif column == "Preview":
                    v = self.get_data().loc[index.row(), column]
                    return self.get_data().loc[index.row(), column].split("/")[-1] \
                        if len(v.split("/")) > 1 else v

                elif column == "Tags":
                    return self.get_data().loc[index.row(), column]
                elif column == "Cards" or column == "id":
                    return str(self.get_data().loc[index.row(), column])

                else:
                    return self.get_data().loc[index.row(), column]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.CheckStateRole and column == "id":
                self._data.loc[index.row(), "Selected"] = value
                self.dataChanged.emit(index, index, [role])
                if all(self.get_data()["Selected"]):
                    self.oldest_settings.Upload_SelectAll_CheckBox.setChecked(True)
                else:
                    self.oldest_settings.Upload_SelectAll_CheckBox.setChecked(False)
                return True
            self._data.loc[index.row(), column] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def setDataFuncs(self, id, column, value):
        self._data[self._data.id == id][column] = value

    def insertRows(self, count: int = 1, parent: QModelIndex = ..., row_content=None, **kwargs) -> bool:
        if not row_content:
            row_content = {}
        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count + count - 1)
        UploadModel.default_content["User"] = app_settings_uploaders.def_account
        for col in self.get_data().columns:
            if col == "id":
                self._data.loc[row_count, col] = row_count + 1
                continue
            if col in row_content.keys() and row_content[col] is not None:
                self._data.loc[row_count, col] = row_content[col]
            else:
                self._data.loc[row_count, col] = UploadModel.default_content[col]
        row_count += count
        self.endInsertRows()
        if "Url" in kwargs.keys():
            self.paths.append(kwargs["Url"])
        self.update()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data = self._data.drop(index=row)
        self._data.reset_index(drop=True, inplace=True)
        self.reset_ids()
        self.endRemoveRows()
        self.update()
        return True

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = [i for i in range(1, self.rowCount() + 1)]
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data


class UploadersUsersModel(QAbstractTableModel):
    columns = ['id', 'Account', 'Gmail']

    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.update()

    def update(self):
        self._data = pd.DataFrame(columns=UploadersUsersModel.columns)
        self._data["Account"] = app_settings_uploaders.accounts.keys()
        self._data["Gmail"] = app_settings_uploaders.accounts.values()
        self._data["id"] = list(map(str, map(lambda x: x + 1, self._data.index)))
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] == "id" or self._data.columns[index.column()] == "Gmail":
            flags = Qt.ItemIsEnabled
        else:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return flags

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            elif orientation == Qt.Vertical:
                return ">"

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.DisplayRole:
                if column == "Gmail":
                    return f'{self.get_data().loc[index.row(), column]}@gmail.com'
                else:
                    return self.get_data().loc[index.row(), column]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = list(self._data.keys())[index.column()]
            if column == "Account" and value != self._data.loc[index.row(), column]:
                if value not in list(self.get_data()["Account"]):
                    self._data.loc[index.row(), column] = value
                    self.dataChanged.emit(index, index, [role])
                    return True
                else:
                    error_func("This Account name is already used")
        return False

    def insertRows(self, row: tuple, parent: QModelIndex = ..., **kwargs) -> bool:
        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count)
        self._data.loc[row_count] = [str(row_count), row[0], row[1], False]
        row_count += 1
        self.endInsertRows()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        row_count = self.rowCount()
        row_count -= 1
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data.drop(index=row)
        self._data.reset_index(drop=True, inplace=True)
        self.reset_ids()
        self.endRemoveRows()
        self.update()
        return True

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = [i for i in range(1, self.rowCount() + 1)]
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data


class OpenFileLocationDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, table=None, ext=None):
        self.table = table
        self.ext = ext
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        if event.type() in [event.MouseButtonDblClick, event.MouseButtonDblClick, event.MouseButtonDblClick,
                            event.MouseButtonDblClick]:
            open_location(table=self.table, index=self.table.currentIndex().row(), ext=self.ext)
        return super().editorEvent(event, model, option, index)


def open_location(table, index, ext: str):
    exts = {
        "Video": video_extensions,
        "Preview": image_extensions,
        "Text": text_extensions
    }
    file, _ = QFileDialog.getOpenFileName(None, f"Select {ext.capitalize()}", "",
                                          f"{ext.capitalize()} Files ({' '.join('*' + ex for ex in exts[ext.capitalize()])})")
    table.model()._data.at[index, ext.capitalize()] = file
    table.update()


def add_video_for_uploading(table: QTableView, path, user=None):
    if path in table.model().paths:
        return
    if user is None:
        user = app_settings_uploaders.def_account
    video = find_files(video_extensions, folder=path)
    title = find_files(text_extensions, folder=path, name="Title")
    description = find_files(text_extensions, folder=path, name="Description")
    playlist = find_files(text_extensions, folder=path, name="Playlist")
    preview = find_files(image_extensions, folder=path)
    tags = find_files(text_extensions, folder=path, name="Tags")
    table.model().insertRows(row_content={"User": user,
                                          "Video": video,
                                          "Title": title,
                                          "Description": description,
                                          "Playlist": playlist,
                                          "Preview": preview,
                                          "Tags": tags},
                             Url=path)
