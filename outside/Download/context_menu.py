from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenu, QAbstractItemView

from outside.context_menu import add_remove_row, add_option_open_link


def download_context_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        if table.currentIndex().column() == 4:
            add_option_open_link(menu, table)
    add_remove_row(menu, ind, table, None)
    cursor = QtGui.QCursor()
    menu.exec_(cursor.pos())