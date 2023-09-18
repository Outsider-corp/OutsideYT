import typing

import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import QModelIndex, QAbstractTableModel, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QStyledItemDelegate, QProgressBar, QWidget, QVBoxLayout

import OutsideYT
from OutsideYT import app_settings_watchers
from outside.message_boxes import error_func


class WatchModel(QAbstractTableModel):
    columns = ["id", "Progress", "Watchers Group", "Count", "Video", "Channel", "Duration", "Link", "Selected"]

    default_content = {"id": None, "Progress": 0,
                       "Watchers Group": app_settings_watchers.def_group, "Count": 0,
                       "Video": "", "Channel": "", "Duration": "0", "Link": "", "Selected": True}

    def __init__(self, data=None, oldest_settings=None):
        QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=WatchModel.columns)
        self._data = data
        self.paths = []
        self.oldest_settings = oldest_settings

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled
        if self._data.columns[index.column()] == "id":
            flags |= Qt.ItemIsUserCheckable
        else:
            flags |= Qt.ItemIsSelectable
            if self._data.columns[index.column()] in ["Link", "Watchers Group"]:
                flags |= Qt.ItemIsEditable
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
            if role == Qt.DisplayRole:
                if column == "Selected":
                    return
                if column == "Duration":
                    duration = ""
                    dur_sec = int(self.get_data().loc[index.row(), column])
                    if dur_sec > 3600:
                        duration += f'{dur_sec // 3600}:'
                        dur_sec %= 3600
                    duration += f'{dur_sec // 60}:{dur_sec % 60}'
                    return duration

                elif column == "Count":
                    return len(app_settings_watchers.groups[self.get_data().loc[index.row(), "Watchers Group"]])

                else:
                    return self.get_data().loc[index.row(), column]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = list(self._data.keys())[index.column()]
            if role == Qt.CheckStateRole and column == "id":
                self._data.loc[index.row(), "Selected"] = value
                self.dataChanged.emit(index, index, [role])
                if all(self.get_data()["Selected"]):
                    self.oldest_settings.Watch_SelectAll_CheckBox.setChecked(True)
                else:
                    self.oldest_settings.Watch_SelectAll_CheckBox.setChecked(False)
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
        WatchModel.default_content["Watchers Group"] = app_settings_watchers.def_group
        for col in self.get_data().columns:
            if col == "id":
                self._data.loc[row_count, col] = row_count + 1
                continue
            if col in row_content.keys() and row_content[col] is not None:
                self._data.loc[row_count, col] = row_content[col]
            else:
                self._data.loc[row_count, col] = WatchModel.default_content[col]
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

    def removeAllRows(self, *args, **kwargs):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self._data = pd.DataFrame(columns=WatchModel.columns)
        self.endRemoveRows()
        self.update()
        return True

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = [i for i in range(1, self.rowCount() + 1)]
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data

    def update_progress_bar(self, index, value):
        self._data.loc[index, "Progress"] = value
        self.update()


class WatchersUsersModel(QAbstractTableModel):
    columns = ['id', 'Account', 'Gmail', 'Group']
    default_group = "No group"

    def __init__(self):
        QAbstractTableModel.__init__(self)
        self._data = pd.DataFrame(columns=WatchersUsersModel.columns)
        self.update()

    def update(self):
        temp_df = pd.DataFrame([(acc, mail, group) for group, accounts in
                                app_settings_watchers.groups.items() for
                                acc, mail in accounts.items()], columns=["Account", "Gmail", "Group"])
        temp_df["id"] = list(map(lambda x: str(x + 1), temp_df.index))
        self._data = temp_df.reindex(columns=WatchersUsersModel.columns)
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
            else:
                self._data.loc[index.row(), column] = value
                self.dataChanged.emit(index, index, [role])
                return True
        return False

    def insertRows(self, row: tuple, parent: QModelIndex = ..., **kwargs) -> bool:
        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count)
        self._data.loc[row_count] = [str(row_count), *row]
        self.endInsertRows()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
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


class WatchersGroupsModel(QAbstractTableModel):
    columns = ['id', 'Group', "New Group name"]

    def __init__(self):
        QAbstractTableModel.__init__(self)
        self._data = pd.DataFrame(columns=WatchersGroupsModel.columns)
        self._data["Group"] = app_settings_watchers.groups.keys()
        self._data["New Group name"] = ''
        self._data["id"] = list(map(lambda x: str(x + 1), self._data.index))
        self.update()

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] in ["id", "Group"]:
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
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            elif orientation == Qt.Vertical:
                return ">"

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.DisplayRole:
                return self.get_data().loc[index.row(), column]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = list(self._data.keys())[index.column()]
            if column == "New Group name" and value != self.get_data().loc[index.row(), column]:
                if value not in list(self.get_data()["Group"]):
                    self._data.loc[index.row(), column] = value
                    self.dataChanged.emit(index, index, [role])
                    return True
                else:
                    error_func("This group name is already used")
        return False

    def insertRows(self, group: str = None, count: int = 1, parent: QModelIndex = ..., **kwargs) -> bool:
        if group is None:
            groupname = "New Group"
            num = 0
            while True:
                if OutsideYT.app_settings_watchers.add_group(f"{groupname} {num}", error_ignore=True):
                    group = f"{groupname} {num}"
                    break
                num += 1

        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count + count - 1)
        self._data.loc[row_count] = [row_count + 1, group, ""]
        if kwargs:
            for col in self.get_data().columns:
                if col == "id":
                    continue
                if col in kwargs.keys() and kwargs[col] is not None:
                    self._data.loc[row_count, col] = kwargs[col]
        row_count += count
        self.endInsertRows()
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


class ProgressBarDelegate(QStyledItemDelegate):

    # def __init__(self, parent):
    #     super().__init__(parent)

    def createEditor(self, parent, option, index):
        # progress_bar = QProgressBar(parent)
        # progress_bar.setProperty("value", 0)
        # progress_bar.setTextVisible(True)
        # progress_bar.setAlignment(Qt.AlignLeft)
        # progress_bar.setMinimum(0)
        # progress_bar.setMaximum(100)
        # progress_bar.setValue(0)
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(9)
        # progress_bar.setFont(font)

        progress_bar = QProgressBar(parent)
        progress_bar.setRange(0, 100)
        progress_bar.setAlignment(Qt.AlignLeft)
        # progress_bar = ProgressWidget(parent)
        return progress_bar

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setValue(int(value))

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.DisplayRole)


class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        self.value_ = 0

    def value(self):
        return self.value_

    def setValue(self, value):
        self.value_ = value
        self.progress_bar.setValue(value)