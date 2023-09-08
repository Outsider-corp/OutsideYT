from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStyleOptionViewItem


class InLineEditDelegate(QtWidgets.QItemDelegate):
    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        return super(InLineEditDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(str(text))


class HeaderView(QtWidgets.QHeaderView):
    def __init__(self, parent=None, def_size=50):
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
        if [self.visualIndex(i) for i in range(self.parent().model().rowCount())] != self.visualIndexes:
            self.visualIndexes = [self.visualIndex(i) for i in range(self.parent().model().rowCount())]
            self.parent().model().reset_ids(map(lambda x: x + 1, self.visualIndexes))


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


def table_universal(table):
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
    return table


def remove_row(table, del_from_settings=None):
    if del_from_settings:
        del_from_settings()
    table.model().removeRow(table.currentIndex().row())
    table.update()
    table.parent().update()
