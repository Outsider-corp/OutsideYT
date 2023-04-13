import os
import sys
import typing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem
import pandas as pd
from OutsideYT import app_settings


class UploadModel(QtCore.QAbstractTableModel):
    columns = ["id", "Selected", "User", "Title", "Publish", "Video", "Description",
               "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
               "FileTitle"]

    default_content = [None, True, app_settings.def_account, "Title", "Now", "select video", "", "", "", "", "random",
                       2, "Private",
                       False]


    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=UploadModel.columns)
        self._data = data

    def flags(self, index: QModelIndex):
        # flags = QtCore.Qt.ItemIsSelectable
        if self._data.columns[index.column()] == "id":
            flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        else:
            flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        return flags

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal and self._data.columns[section] != "Selected":
                return self._data.columns[section]
            elif orientation == QtCore.Qt.Vertical:
                return ">"

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == QtCore.Qt.CheckStateRole and column == "id":
                return QtCore.Qt.Checked if self._data.loc[index.row(), "Selected"] else QtCore.Qt.Unchecked
            if role == QtCore.Qt.DisplayRole:
                if column == "Selected":
                    return
                if column == "Publish":
                    return self._data.loc[index.row(), column]

                elif column == "Video":
                    return self._data.loc[index.row(), column]

                elif column == "Description":
                    return self._data.loc[index.row(), column]

                elif column == "Playlist":
                    return self._data.loc[index.row(), column]

                elif column == "Preview":
                    return self._data.loc[index.row(), column]

                elif column == "Tags":
                    return self._data.loc[index.row(), column]

                elif column == "Ends":
                    return self._data.loc[index.row(), column]

                elif column == "Cards":
                    return self._data.loc[index.row(), column]

                elif column == "FileTitle":
                    return self._data.loc[index.row(), column]

                elif column == "Delete":
                    return self._data.loc[index.row(), column]
                else:
                    return self._data.loc[index.row(), column]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == QtCore.Qt.CheckStateRole and column == "id":
                self._data.loc[index.row(), "Selected"] = value
                self.dataChanged.emit(index, index, [role])
                return True
            self._data.loc[index.row(), column] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def insertRow(self, row: list, index: QModelIndex = None):
        self.insertRows()
        self.beginInsertRows()
        if not index:
            index = self.rowCount()
        else:
            index = index.row()
        self._data.loc[index] = [str(index) if i is None else i for i in row]
        self.endInsertRows()
        return True

    def insertRows(self, count: int = 1, parent: QModelIndex = ..., **kwargs) -> bool:
        row_count = self.rowCount()
        self.beginInsertRows(QModelIndex(), row_count, row_count + count - 1)
        for i in range(count):
            self._data.loc[row_count + i] = [str(row_count + i + 1) if j is None else j for j in
                                             UploadModel.default_content]
        row_count += count
        self.endInsertRows()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        row_count = self.rowCount()
        row_count -= 1
        self.beginRemoveRows(QModelIndex(), row_count, row_count)
        self._data.drop(index=self._data.loc[row])
        self.reset_ids()
        self.endRemoveRows()
        return True

    def reset_ids(self, new_list):
        self._data.id = list(map(str, map(lambda x: x + 1, new_list)))

    def get_data(self):
        return self._data


class HeaderView(QtWidgets.QHeaderView):
    def __init__(self, parent=None):
        super().__init__(QtCore.Qt.Vertical, parent)
        self.setSectionsClickable(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QHeaderView.InternalMove)
        self.setCascadingSectionResizes(False)
        self.setDefaultSectionSize(50)
        self.setMinimumSectionSize(40)
        self.setStretchLastSection(False)
        self.setSectionsMovable(True)
        self.visualIndexes = [self.visualIndex(i) for i in range(self.parent().model().rowCount())]

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        # for i in range(self.parent().model().rowCount()):
        #     print(f"{self.visualIndex(i)} -> {self.parent().model().get_data().id.iloc[i]}")
        if [self.visualIndex(i) for i in range(self.parent().model().rowCount())] != \
                self.visualIndexes:
            self.visualIndexes = [self.visualIndex(i) for i in range(self.parent().model().rowCount())]
            self.parent().model().reset_ids(self.visualIndexes)

class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, items):
        super().__init__()
        self.items = items

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(self.items)
        editor.setCurrentText(index.model().data(index, QtCore.Qt.DisplayRole))
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)
        model.setData(index, value, QtCore.Qt.DisplayRole)

    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QtWidgets.QStyledItemDelegate.NoHint)
