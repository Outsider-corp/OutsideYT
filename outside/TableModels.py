from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget

from outside.message_boxes import warning_func


class InLineEditDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem',
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


def remove_selected_rows(table, del_from_settings=None, type_deleting=''):
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
