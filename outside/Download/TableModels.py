import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import pandas as pd


class DownloadModel(QAbstractTableModel):
    columns = ['id', 'Video', 'Channel', 'Duration', 'Link', 'Selected']

    default_content = {'id': None, 'Video': '', 'Channel': '', 'Duration': '0', 'Link': '', 'Selected': True}

    def __init__(self, data=None, oldest_settings=None) -> None:
        QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=DownloadModel.columns)
        self._data = data
        self.oldest_settings = oldest_settings

    def update(self):
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled
        if self._data.columns[index.column()] == 'id':
            flags |= Qt.ItemIsUserCheckable
        else:
            flags |= Qt.ItemIsSelectable
            if self._data.columns[index.column()] == "Link":
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
                    duration += f'{dur_sec // 60}:{dur_sec % 60}'
                    return duration
                else:
                    return self.get_data().loc[index.row(), column]
            return None
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

    def insertRows(self, count: int = 1, parent: QModelIndex = ..., row_content=None, **kwargs) -> bool:
        if not row_content:
            row_content = {}
        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count + count - 1)
        for col in self.get_data().columns:
            if col == 'id':
                self._data.loc[row_count, col] = row_count + 1
                continue
            if col in row_content and row_content[col] is not None:
                self._data.loc[row_count, col] = row_content[col]
            else:
                self._data.loc[row_count, col] = DownloadModel.default_content[col]
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

    def update_progress_bar(self, index, value, viewport):
        self._data.loc[index, 'Progress'] = value
        self.update()
        viewport.update()

    def reset_progress_bars(self):
        self._data['Progress'] = 0
        self.update()