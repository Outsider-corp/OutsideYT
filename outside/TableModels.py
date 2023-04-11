import os
import sys
import typing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from PyQt5.QtCore import QModelIndex
import pandas as pd
from OutsideYT import app_settings


class UploadModel(QtCore.QAbstractTableModel):
    columns = ["id", "Select", "User", "Title", "Publish", "Video", "Description",
               "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
               "FileTitle"]

    default_content = [None, True, app_settings.def_account, "Title", "Now", "select video", "", "", "", "", "random",
                       2, "0",
                       False]

    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        if data is None:
            data = pd.DataFrame(columns=UploadModel.columns)
        self._data = data

    def flags(self, index: QModelIndex):
        if self._data.columns[index.column()] != "id":
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.index)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data.columns)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal and self._data.columns[section] != "Select":
                return self._data.columns[section]
            elif orientation == QtCore.Qt.Vertical:
                return ">"

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        column = self._data.columns[index.column()]
        if role == QtCore.Qt.DisplayRole:
            if column == "Select":
                pass
            elif column == "User":
                cell = QtWidgets.QComboBox()
                cell.addItems(list(app_settings.accounts.keys()))
                return cell

            elif column == "Publish":
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

            elif column == "Access":
                return self._data.loc[index.row(), column]

            elif column == "FileTitle":
                return self._data.loc[index.row(), column]

            elif column == "Delete":
                return self._data.loc[index.row(), column]
            else:
                return self._data.loc[index.row(), column]

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            sel_column = self._data.columns[index.column()]
            self._data.loc[index.row(), sel_column] = value
            self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole,))
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

    # def moveRows(self, sourceParent: QModelIndex, sourceRow: int, count: int, destinationParent: QModelIndex,
    #              destinationChild: int) -> bool:
    #     if destinationChild < sourceRow:
    #         rows = sorted(range(destinationChild, destinationChild + count),
    #                       reverse=True)
    #     else:
    #         rows = range(destinationChild, destinationChild + count)
    #     print("!!!!!!!")
    #     self.beginMoveRows(sourceParent, sourceRow, sourceRow + count - 1, destinationParent, destinationChild)
    #     for row in rows:
    #         self._data.insert(destinationChild, self._data.pop(row), )
    #     self.endMoveRows()

    def reset_ids(self, new_list):
        self._data.id = list(map(str, map(lambda x: x+1, new_list)))

    def get_data(self):
        return self._data


class HeaderView(QtWidgets.QHeaderView):
    def __init__(self, parent=None):
        super().__init__(QtCore.Qt.Vertical, parent)
        self.setSectionsClickable(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QHeaderView.InternalMove)
        self.setCascadingSectionResizes(False)
        self.setDefaultSectionSize(40)
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


class HeaderDelegate(QtWidgets.QAbstractItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pressed_index = None
        print("CREATED")

    def paint(self, painter, option, index):
        print("PAINT")
        text = index.model().headerData(index.column(), QtCore.Qt.Vertical, QtCore.Qt.DisplayRole)
        painter.drawText(option.rect, QtCore.Qt.AlignCenter, text)
        # super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            print("PRESS")
            self._pressed_index = index
            return True
        if event.type() == event.MouseMove and self._pressed_index:
            print("MOVE")
            rect = model.headerData(self._pressed_index.column(), QtCore.Qt.Vertical, QtCore.Qt.DisplayRole)
            mime_data = model.mimeData([self._pressed_index])
            drag = QtGui.QDrag(option.widget)
            drag.setMimeData(mime_data)
            # pixmap = option.widget.viewport().grab(rect)
            # drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - option.rect.topLeft())
            drag.exec_()
            # self._pressed_index = None
            return True
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            print("RELEASE")
            model.moveRows(QtCore.QModelIndex(), self._pressed_index.row(), self._pressed_index.row(),
                           QtCore.QModelIndex(), index.row() if index.isValid() else model.rowCount())
            self._pressed_index = None
            return True
        return super().editorEvent(event, model, option, index)

# class UploadTableUnit:
#     index = 0
#
#     def __init__(self, user=None, video="-def", preview="-def",
#                  title="-def", description="-def", playlist="-def",
#                  tags="-def", ends="random", cards=1, publ_time=None,
#                  access=0, save_title=False):
#         self.index = UploadTableUnit.index + 1
#         self.user = user
#         self.folder = user
#         self.video = video
#         self.preview = preview
#         self.title = title
#         self.description = description
#         self.playlist = playlist
#         self.tags = tags
#         self.ends = ends
#         self.cards = cards
#         self.publ_time = publ_time
#         self.access = access
#         self.save_title = save_title
#
#     def user(self):
#         pass
#
#     @classmethod
#     def find_files(args: list, folder: str, name: str = ""):
#         for file in os.listdir(folder):
#             if file.endswith(tuple(args)) and file.startswith(name):
#                 if ".txt" in args:
#                     with open(os.path.join(folder, file), "r", encoding="UTF-8") as f:
#                         return f.read()
#                 return file
#         print("File not founded")
#         return None
#
#
# class WatchTableUnit:
#     pass
#
#
# class DownloadTableUnit:
#     pass
