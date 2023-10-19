import typing

import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget, QStyledItemDelegate

from outside.OYT_Settings import app_settings_uploaders, app_settings_download
from outside.message_boxes import warning_func, error_func
from outside.views_py import TextEdit_Widget


class InLineEditDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem,
                     index: QtCore.QModelIndex) -> QWidget:
        return super(InLineEditDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(str(text))


class HeaderView(QtWidgets.QHeaderView):
    def __init__(self, parent=None, def_size=30, replace=True) -> None:
        self.replace = replace
        super().__init__(QtCore.Qt.Vertical, parent)
        self.setSectionsClickable(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QHeaderView.InternalMove)
        self.setCascadingSectionResizes(False)
        self.setDefaultSectionSize(def_size)
        self.setMinimumSectionSize(30)
        self.setStretchLastSection(False)
        self.setSectionsMovable(True)
        self.visualIndexes = [self.visualIndex(i) for i in range(self.parent().model().rowCount())]

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        if self.replace and [self.visualIndex(i) for i in
                             range(self.parent().model().rowCount())] != self.visualIndexes:
            self.visualIndexes = [self.visualIndex(i) for i in
                                  range(self.parent().model().rowCount())]
            self.parent().model().reset_ids((x + 1 for x in self.visualIndexes))


class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent, items) -> None:
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
    def __init__(self, parent=None) -> None:
        super(SpinBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(4)
        return editor

    def setEditorData(self, editor: QtWidgets.QSpinBox, index):
        value = index.model().get_data().loc[index.row(), 'Cards']
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


def table_universal(table, font_size: int = 11):
    table.setFrameShape(QtWidgets.QFrame.StyledPanel)
    table.setFrameShadow(QtWidgets.QFrame.Sunken)
    table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
    table.setAlternatingRowColors(False)
    table.setTextElideMode(QtCore.Qt.ElideRight)
    table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
    table.setGridStyle(QtCore.Qt.SolidLine)
    table.horizontalHeader().setCascadingSectionResizes(False)
    table.horizontalHeader().setStretchLastSection(False)
    table.verticalHeader().setCascadingSectionResizes(False)
    table.verticalHeader().setStretchLastSection(False)
    table.verticalHeader().setSectionsMovable(True)
    table.setDragEnabled(True)
    table.setDropIndicatorShown(True)
    table.setDefaultDropAction(QtCore.Qt.MoveAction)
    table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    table.viewport().setAcceptDrops(True)
    table.setDragDropOverwriteMode(False)
    table.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter)
    table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)

    table.setItemDelegate(InLineEditDelegate())

    font = QtGui.QFont()
    font.setFamily('Arial')
    font.setPointSize(font_size)
    table.setFont(font)

    return table


def remove_row(table, del_from_settings=None):
    if del_from_settings:
        del_from_settings()
    table.model().removeRow(table.currentIndex().row())
    table.update()
    table.parent().update()


def remove_selected_rows(table, del_from_settings=None, type_deleting: str = ''):
    if warning_func('Are you sure you want to delete UNSELECTED rows?'):
        num_rows = table.model().rowCount()
        data = table.model().get_data()
        for index in range(num_rows - 1, -1, -1):
            if not data.loc[index, 'Selected']:
                if del_from_settings and type_deleting:
                    del_from_settings(data.loc[index, type_deleting])
                table.model().removeRow(int(data.loc[index, 'id']) - 1)
                table.update()
                table.parent().update()


def remove_all_rows(table: QtWidgets.QTableView):
    if warning_func('Are you sure you want to delete ALL rows?'):
        table.model().removeAllRows()
        table.update()
        table.parent().update()


class UsersModel(QAbstractTableModel):
    columns = ['id', 'Account', 'Gmail']

    def __init__(self, table_type: str) -> None:
        QAbstractTableModel.__init__(self)
        self._table_type = table_type
        self.settings = app_settings_uploaders if self.table_type == "upload" else \
            app_settings_download
        self.update()

    @property
    def table_type(self):
        return self._table_type

    def update(self):
        self._data = pd.DataFrame(columns=UsersModel.columns)
        self._data['Account'] = self.settings.accounts.keys()
        self._data['Gmail'] = self.settings.accounts.values()
        self._data['id'] = list(map(str, (x + 1 for x in self._data.index)))
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


class EditTextDelegate(QStyledItemDelegate):

    def __init__(self, parent=None, text_type: str = ''):
        super().__init__(parent)
        self.text_type = text_type
        self.par = parent

    def createEditor(self, parent, option, index):
        text = index.model().data(index, Qt.DisplayRole)
        video_name = index.model().get_data().loc[index.row(), 'Title']
        editor = EditTextWidget(text, video_name, self.text_type, self.par)
        return editor

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        cursor = QCursor()
        editor.move(cursor.pos())
    def setModelData(self, editor, model, index):
        if self.text_type.lower() == 'tags':
            text = editor.text.replace(', ', ',')
        else:
            text = editor.text
        model.setData(index, text, Qt.DisplayRole)


class EditTextWidget(QWidget):
    def __init__(self, text: str = '', video_name: str = '', text_type: str = '', parent=None):
        super().__init__()
        self.ui = TextEdit_Widget.Ui_Form()
        self.ui.setupUi(self)
        self.text = text
        self.ui.TextEdit.setPlainText(text)
        self.ui.Type_label.setText(video_name)
        self.setWindowTitle(f"{text_type} Edit")

        self.setMinimumSize(300, 250)

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.accept)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Discard).clicked.connect(self.close)

    def accept(self):
        self.text = self.ui.TextEdit.toPlainText()
        self.close()
