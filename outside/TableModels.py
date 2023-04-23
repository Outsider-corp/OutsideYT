import os
import sys
import typing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem, QStyleFactory
import pandas as pd
from OutsideYT import app_settings_uploaders


class UploadModel(QtCore.QAbstractTableModel):
    columns = ["id", "Selected", "User", "Title", "Publish", "Video", "Description",
               "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
               "Save filename?"]

    default_content = [None, True, app_settings_uploaders.def_account, "", "Now", "select video", "", "", "", "",
                       "random",
                       2, "Private",
                       False]

    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=UploadModel.columns)
        self._data = data

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] == "id" or self._data.columns[index.column()] == "Save filename?":
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
            if role == QtCore.Qt.CheckStateRole:
                if column == "id":
                    return QtCore.Qt.Checked if self._data.loc[index.row(), "Selected"] else QtCore.Qt.Unchecked
                elif column == "Save filename?":
                    if self.get_data().loc[index.row(), "Title"] == "":
                        return QtCore.Qt.Checked if self.get_data().loc[
                            index.row(), "Save filename?"] else QtCore.Qt.Unchecked
            if role == QtCore.Qt.DisplayRole:
                if column == "Selected" or column == "Save filename?":
                    return
                if column == "Publish":
                    return self.get_data().loc[index.row(), column]

                elif column == "Video":
                    return self.get_data().loc[index.row(), column]

                elif column == "Description":
                    return self.get_data().loc[index.row(), column]

                elif column == "Playlist":
                    return self.get_data().loc[index.row(), column]

                elif column == "Preview":
                    return self.get_data().loc[index.row(), column]

                elif column == "Tags":
                    return self.get_data().loc[index.row(), column]
                elif column == "Cards":
                    return str(self.get_data().loc[index.row(), column])

                else:
                    return self.get_data().loc[index.row(), column]

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

    def reset_ids(self, new_list=None):
        if new_list is None:
            new_list = [i + 1 for i in range(self.rowCount())]
        self._data.id = list(map(str, new_list))

    def get_data(self):
        return self._data


class UsersModel(QtCore.QAbstractTableModel):
    columns = ['id', 'Account', 'Gmail']

    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.update()

    def update(self):
        self._data = pd.DataFrame(columns=UsersModel.columns)
        self._data["Account"] = app_settings_uploaders.accounts.keys()
        self._data["Gmail"] = app_settings_uploaders.accounts.values()
        self._data["id"] = list(map(str, map(lambda x: x + 1, self._data.index)))
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] == "id" or self._data.columns[index.column()] == "Gmail":
            flags = QtCore.Qt.ItemIsEnabled
        else:
            flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        return flags

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._data.columns[section]
            elif orientation == QtCore.Qt.Vertical:
                return ">"

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            column = self._data.columns[index.column()]
            if role == QtCore.Qt.DisplayRole:
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
        self.beginRemoveRows(QModelIndex(), row_count, row_count)
        self._data.drop(index=self._data.loc[row])
        self.reset_ids()
        self.endRemoveRows()
        return True

    def reset_ids(self, new_list):
        self._data.id = list(map(str, map(lambda x: x + 1, new_list)))

    def get_data(self):
        return self._data


class InLineEditDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        return super(InLineEditDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(str(text))


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
        if [self.visualIndex(i) for i in range(self.parent().model().rowCount())] != self.visualIndexes:
            self.visualIndexes = [self.visualIndex(i) for i in range(self.parent().model().rowCount())]
            self.parent().model().reset_ids(self.visualIndexes)


class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent, items):
        super().__init__(parent)
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


class SpinBoxDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        super(SpinBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(4)
        return editor

    def setEditorData(self, editor: QtWidgets.QSpinBox, index):
        value = index.model().get_data().loc[index.row(), "Cards"]
        if value is not None:
            editor.setValue(int(value))
        else:
            editor.setValue(2)

    def setModelData(self, editor: QtWidgets.QSpinBox, model, index):
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, QtCore.Qt.EditRole)
        model.setData(index, value, QtCore.Qt.DisplayRole)

    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QtWidgets.QStyledItemDelegate.NoHint)


def error_func(text):
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText(text)
    error_dialog.setStyle(QStyleFactory.create("Fusion"))
    error_dialog.setWindowTitle("Error")
    error_dialog.exec_()
