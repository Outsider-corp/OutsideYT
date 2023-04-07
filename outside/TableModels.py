import os
import sys
import typing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from PyQt5.QtCore import QModelIndex
import pandas as pd

from OutsideYT import app_settings


class UploadModel(QtCore.QAbstractTableModel):
    columns = ["Select", "id", "User", "Title", "Publish", "Video", "Description",
               "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
               "FileTitle"]

    default_content = [True, None, app_settings.def_account, "Title", "Now", "select video", "", "", "", "", "random",
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
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole \
                and self._data.columns[section] != "Select":
            return self._data.columns[section]

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
            self._data.loc[row_count + i] = [str(row_count + i+1) if j is None else j for j in
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

    def reset_ids(self):
        self._data.id = self._data.index

    def get_data(self):
        return self._data


class RowDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()
        elif event.type() == event.MouseMove and event.buttons() == QtCore.Qt.LeftButton:
            if (event.pos() - self.drag_start_position).manhattanLength() > QtWidgets.QApplication.startDragDistance():
                drag = QtGui.QDrag(self.parent())
                mime_data = QtCore.QMimeData()
                row = index.row()


                endata = QtCore.QByteArray()
                stream = QtCore.QDataStream(endata, QtCore.QIODevice.WriteOnly)
                if index.isValid():
                    itemdata = model.itemData(index)
                    print(itemdata)
                    stream.writeInt32(index.row())
                    stream.writeInt32(index.column())
                    stream.writeQVariant((QtCore.QVariant(itemdata[QtCore.Qt.DisplayRole])))



                mime_data.setData("application/x-qabstractitemmodeldatalist", endata)
                # mime_data.setData("application/x-qabstractitemmodeldatalist", model.itemData(index))
                mime_data.setData("application/x-qabstractitemmodeldatalist", bytes())
                drag.setMimeData(mime_data)
                drag.exec_()
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
