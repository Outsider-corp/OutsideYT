from functools import partial

from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication

from outside import Dialogs


def upload_context_menu(pos, parent, table: QtWidgets.QAbstractItemView):
    menu = QtWidgets.QMenu(parent)
    print(pos)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes() and table.currentIndex().column() == 4:
        set_time = menu.addAction("Set Publish Time")
        set_time.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_FileDialogDetailedView))
        set_time.triggered.connect(
            partial(Dialogs.set_upload_time_for_video, parent=parent, table=table, video_id=table.currentIndex().row()))
        if table.model().get_data().at[table.currentIndex().row(), "Publish"] != "Now":
            remove_time = menu.addAction("Remove Publish Time")
            remove_time.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))

            def remove_time_func():
                table.model()._data.at[table.currentIndex().row(), "Publish"] = "Now"
                table.update()

            remove_time.triggered.connect(remove_time_func)
        menu.addSeparator()
    add_data = menu.addAction("Add New Row")
    add_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown))
    add_data.triggered.connect(lambda: table.model().insertRows())
    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction("Remove Row")
        remove_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton))
        remove_data.triggered.connect(lambda: table.model().removeRow(table.currentIndex().row()))
    cursor = QtGui.QCursor()
    menu.exec_(cursor.pos())
