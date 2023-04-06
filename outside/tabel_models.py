import os
import typing

from PyQt5 import QtCore
from PyQt5 import Qt
import pandas as pd


class UploadModel(QtCore.QAbstractTableModel):
    columns = ["id", "User", "Title", "Publ time", "Video", "Description",
               "Playlist", "Preview", "Tags", "Ends", "Cards", "Access",
               "Save title?", "Delete", "Select"]

    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        if not data:
            data = pd.DataFrame(columns=UploadModel.columns)
        self.data = data

    def flags(self, index: QtCore.QModelIndex) -> Qt.ItemFlags:
        if index.column() > 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self.data.index)

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return len(self.data.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == QtCore.Qt.Horizontal and role== QtCore.Qt.DisplayRole:
            return self.data.columns[section]

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any:
        pass






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
