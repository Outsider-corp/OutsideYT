import typing

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from outside.functions import get_video_link


class DownloadModel(QAbstractTableModel):
    columns = ['id', 'Video', 'Channel', 'Duration', 'Link', 'Selected', '_download_info']

    default_content = {'id': None, 'Video': '', 'Channel': '', 'Duration': '0', 'Link': '',
                       'Selected': True, '_download_info': None}

    def __init__(self, data=None, oldest_settings=None, table_progress_bar=None,
                 table_progress_label=None) -> None:
        QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=DownloadModel.columns)
        self._data = data
        self.oldest_settings = oldest_settings
        self._table_progress_bar = table_progress_bar
        self._table_progress_label = table_progress_label

    @property
    def table_type(self):
        return 'download'

    @property
    def progress_bar(self):
        return self._table_progress_bar

    @property
    def progress_label(self):
        return self._table_progress_label

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled
        if self._data.columns[index.column()] == 'id':
            flags |= Qt.ItemIsUserCheckable
        else:
            flags |= Qt.ItemIsSelectable
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
                if column in ['Selected', '_download_info']:
                    return None
                if column == 'Duration':
                    duration = ''
                    dur_sec = int(self.get_data().loc[index.row(), column])
                    if dur_sec > 3600:
                        duration += f'{dur_sec // 3600}:'
                        dur_sec %= 3600
                    duration += f'{dur_sec // 60:02d}:{dur_sec % 60:02d}'
                    return duration
                if column == 'Link':
                    link = self.get_data().loc[index.row(), column]
                    return get_video_link(link, 'watch')
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
        new_row = pd.Series(index=self.get_data().columns)
        for col in new_row.index:
            if col == 'id':
                new_row[col] = row_count + 1
                continue
            if col in row_content and row_content[col] is not None:
                new_row[col] = row_content[col]
            else:
                new_row[col] = DownloadModel.default_content[col]
        self._data.loc[row_count] = new_row
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
        self._data = pd.DataFrame(columns=DownloadModel.columns)
        self.endRemoveRows()
        self.update()
        return True

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = list(range(1, self.rowCount() + 1))
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data

