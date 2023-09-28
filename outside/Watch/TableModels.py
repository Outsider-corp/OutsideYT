import typing

import pandas as pd
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtWidgets import (
    QStyledItemDelegate,
)

from outside.message_boxes import error_func
from OutsideYT import app_settings_watchers


class WatchModel(QAbstractTableModel):
    columns = ['id', 'Progress', 'Watchers Group', 'Count', 'Video', 'Channel', 'Duration', 'Link',
               'Selected']

    default_content = {'id': None, 'Progress': 0,
                       'Watchers Group': app_settings_watchers.def_group, 'Count': 0,
                       'Video': '', 'Channel': '', 'Duration': '0', 'Link': '', 'Selected': True}

    def __init__(self, data=None, oldest_settings=None, main_progress_bar=None,
                 tableview=None) -> None:
        QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=WatchModel.columns)
        self._data = data
        self.oldest_settings = oldest_settings
        self._main_progress_bar = main_progress_bar
        self._tableview = tableview

    def update(self):
        self.layoutChanged.emit()

    @property
    def table_type(self):
        return "watch"

    @property
    def progress_bar(self):
        return self._main_progress_bar

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled
        if self._data.columns[index.column()] == 'id':
            flags |= Qt.ItemIsUserCheckable
        else:
            flags |= Qt.ItemIsSelectable
            if self._data.columns[index.column()] in ['Watchers Group']:
                flags |= Qt.ItemIsEditable
        return flags

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and self._data.columns[section] != 'Selected':
                return self._data.columns[section]
            elif orientation == Qt.Vertical:
                return '>'
            return None
        return None

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.CheckStateRole and column == 'id':
                return Qt.Checked if self._data.loc[index.row(), 'Selected'] else Qt.Unchecked
            if role == Qt.DisplayRole:
                if column == 'Selected':
                    return None
                if column == 'Duration':
                    duration = ''
                    dur_sec = int(self.get_data().loc[index.row(), column])
                    if dur_sec > 3600:
                        duration += f'{dur_sec // 3600}:'
                        dur_sec %= 3600
                    duration += f'{dur_sec // 60:02d}:{dur_sec % 60:02d}'
                    return duration

                elif column == 'Count':
                    return len(app_settings_watchers.groups[self.get_data().loc[index.row(),
                                                                                'Watchers Group']])

                else:
                    return self.get_data().loc[index.row(), column]
        return None

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = list(self._data.keys())[index.column()]
            if role == Qt.CheckStateRole and column == 'id':
                self._data.loc[index.row(), 'Selected'] = value
                self.dataChanged.emit(index, index, [role])
                if all(self.get_data()['Selected']):
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

    def insertRows(self, count: int = 1, parent: QModelIndex = ..., row_content=None,
                   **kwargs) -> bool:
        if not row_content:
            row_content = {}
        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count + count - 1)
        WatchModel.default_content['Watchers Group'] = app_settings_watchers.def_group
        for col in self.get_data().columns:
            if col == 'id':
                self._data.loc[row_count, col] = row_count + 1
                continue
            if col in row_content and row_content[col] is not None:
                self._data.loc[row_count, col] = row_content[col]
            else:
                self._data.loc[row_count, col] = WatchModel.default_content[col]
        row_count += count
        self.endInsertRows()
        self.update()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data = self._data.drop(index=row)
        self._data = self._data.reset_index(drop=True)
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
            new_list = list(range(1, self.rowCount() + 1))
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data

    def update_progress_bar(self, index, value):
        self._data.loc[index, 'Progress'] = value
        qindex = self.index(index, 1, QModelIndex())
        self._tableview.update(qindex)

    def reset_progress_bars(self):
        self._data['Progress'] = 0
        self.update()


class WatchersUsersModel(QAbstractTableModel):
    columns = ['id', 'Account', 'Gmail', 'Group']
    default_group = 'No group'

    def __init__(self) -> None:
        QAbstractTableModel.__init__(self)
        self._data = pd.DataFrame(columns=WatchersUsersModel.columns)
        self.update()

    @property
    def table_type(self):
        return "watch"

    def update(self):
        temp_df = pd.DataFrame([(acc, mail, group) for group, accounts in
                                app_settings_watchers.groups.items() for
                                acc, mail in accounts.items()],
                               columns=['Account', 'Gmail', 'Group'])
        temp_df['id'] = [str(x + 1) for x in temp_df.index]
        self._data = temp_df.reindex(columns=WatchersUsersModel.columns)
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] == 'id' or self._data.columns[
            index.column()] == 'Gmail':
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
                return '>'
            return None
        return None

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.DisplayRole:
                if column == 'Gmail':
                    return f'{self.get_data().loc[index.row(), column]}@gmail.com'
                else:
                    return self.get_data().loc[index.row(), column]
            return None
        return None

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = list(self._data.keys())[index.column()]
            if column == 'Account' and value != self._data.loc[index.row(), column]:
                if value not in list(self.get_data()['Account']):
                    self._data.loc[index.row(), column] = value
                    self.dataChanged.emit(index, index, [role])
                    return True
                else:
                    error_func('This Account name is already used')
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
        self._data = self._data.reset_index(drop=True)
        self.reset_ids()
        self.endRemoveRows()
        self.update()
        return True

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = list(range(1, self.rowCount() + 1))
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data


class WatchersGroupsModel(QAbstractTableModel):
    columns = ['id', 'Group', 'New Group name']

    def __init__(self) -> None:
        QAbstractTableModel.__init__(self)
        self._data = pd.DataFrame(columns=WatchersGroupsModel.columns)
        self._data['Group'] = app_settings_watchers.groups.keys()
        self._data['New Group name'] = ''
        self._data['id'] = [str(x + 1) for x in self._data.index]
        self.update()

    @property
    def table_type(self):
        return "watch"

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] in ['id', 'Group']:
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
                return '>'
            return None
        return None

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == Qt.DisplayRole:
                return self.get_data().loc[index.row(), column]
            return None
        return None

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = list(self._data.keys())[index.column()]
            if column == 'New Group name' and value != self.get_data().loc[index.row(), column]:
                if value not in list(self.get_data()['Group']):
                    self._data.loc[index.row(), column] = value
                    self.dataChanged.emit(index, index, [role])
                    return True
                else:
                    error_func('This group name is already used')
        return False

    def insertRows(self, group: str = None, count: int = 1, parent: QModelIndex = ...,
                   **kwargs) -> bool:
        if group is None:
            groupname = 'New Group'
            num = 0
            while True:
                if app_settings_watchers.add_group(f'{groupname} {num}', error_ignore=True):
                    group = f'{groupname} {num}'
                    break
                num += 1

        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count + count - 1)
        self._data.loc[row_count] = [row_count + 1, group, '']
        if kwargs:
            for col in self.get_data().columns:
                if col == 'id':
                    continue
                if col in kwargs and kwargs[col] is not None:
                    self._data.loc[row_count, col] = kwargs[col]
        row_count += count
        self.endInsertRows()
        self.update()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data = self._data.drop(index=row)
        self._data = self._data.reset_index(drop=True)
        self.reset_ids()
        self.endRemoveRows()
        self.update()
        return True

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = list(range(1, self.rowCount() + 1))
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data


class ProgressBarDelegate(QStyledItemDelegate):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.progress_bar = QtWidgets.QStyleOptionProgressBar()
        self.progress_bar.state = QtWidgets.QStyle.State_Enabled
        self.progress_bar.direction = QtWidgets.QApplication.layoutDirection()
        self.progress_bar.minimum = 0
        self.progress_bar.maximum = 100
        self.progress_bar.text = f'{self.progress_bar.progress}%'
        self.progress_bar.textVisible = True
        pal = self.progress_bar.palette
        pal.setColor(QtGui.QPalette.Highlight, QtGui.QColor(189, 0, 0))
        self.progress_bar.palette = pal

    def paint(self, painter, option, index):
        self.progress_bar.rect = option.rect
        self.progress_bar.fontMetrics = QtGui.QFontMetrics(option.font)
        self.progress_bar.progress = int(index.data())
        self.progress_bar.text = f'{self.progress_bar.progress}%'
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ProgressBar,
                                                   self.progress_bar, painter)
