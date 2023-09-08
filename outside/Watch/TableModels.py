import typing

import pandas as pd
from PyQt5.QtCore import QModelIndex, QAbstractTableModel, Qt

import OutsideYT
from OutsideYT import app_settings_watchers
from outside.errors import error_func


class WatchModel(QAbstractTableModel):
    columns = ["id", "Watchers Group", "Count", "Video", "Channel", "Link", "Selected"]

    default_content = {"id": None,
                       "Watchers Group": app_settings_watchers.def_group, "Count": "",
                       "Video": "", "Channel": "", "Link": "", "Selected": True}

    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=WatchModel.columns)
        self._data = data
        self.paths = []

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] == "id":
            flags = Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        elif self._data.columns[index.column()] == "Link":
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        elif self._data.columns[index.column()] in ["Watchers Group", "Count"]:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            flags = Qt.ItemIsSelectable
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
                if column == "Watcher's Group":
                    return self.get_data().loc[index.row(), column]

                elif column == "Video":
                    return self.get_data().loc[index.row(), column]

                elif column == "Channel":
                    return self.get_data().loc[index.row(), column]

                elif column == "Link":
                    return self.get_data().loc[index.row(), column]

                elif column == "Count":
                    return self.get_data().loc[index.row(), column]

                else:
                    return self.get_data().loc[index.row(), column]

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = [i for i in range(self.rowCount())]
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data


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
            new_list = [i + 1 for i in range(self.rowCount())]
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data
