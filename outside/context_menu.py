from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from outside.TableModels import remove_row, remove_selected_rows, remove_all_rows


def add_remove_row(menu, ind, table: QtWidgets.QAbstractItemView, type_deleting: str = ""):

    add_data = menu.addAction("Add New Row")
    add_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown))
    add_data.triggered.connect(lambda: table.model().insertRows())
    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction("Remove Row")
        remove_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton))
        remove_data.triggered.connect(
            partial(remove_row, table=table))
        table.update()
    if "Selected" in table.model().get_data().columns and not all(table.model().get_data()["Selected"]):
        remove_all_data = menu.addAction("Remove Unselected Rows")
        remove_all_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxCritical))
        remove_all_data.triggered.connect(
            partial(remove_selected_rows, table=table, type_deleting=type_deleting))
    if table.model().rowCount():
        menu.addSeparator()
        del_all = menu.addAction("Clear Table")
        del_all.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogResetButton))
        del_all.triggered.connect(partial(remove_all_rows, table=table))
