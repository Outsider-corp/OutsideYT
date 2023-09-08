from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from outside.TableModels import remove_row


def add_remove_row(menu, ind, table: QtWidgets.QAbstractItemView, del_from_settings):
    add_data = menu.addAction("Add New Row")
    add_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown))
    add_data.triggered.connect(lambda: table.model().insertRows())
    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction("Remove Row")
        remove_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton))
        remove_data.triggered.connect(partial(remove_row, table=table, del_from_settings=del_from_settings))
        table.update()
