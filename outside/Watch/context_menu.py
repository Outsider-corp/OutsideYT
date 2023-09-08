from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QApplication, QStyle

import OutsideYT
from outside.context_menu import add_remove_row


def watchers_group_dialogs_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        group = table.model().get_data().loc[table.currentIndex().row(), "Group"]
        add_remove_row(menu, ind, table, partial(OutsideYT.app_settings_watchers.del_group, group=group))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


def watchers_dialogs_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        account = table.model().get_data().loc[table.currentIndex().row(), "Account"]
        group = table.model().get_data().loc[table.currentIndex().row(), "Group"]
        add_remove_row(menu, ind, table, partial(OutsideYT.app_settings_watchers.del_account, group=group,
                                                 login=account))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


def watch_context_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        pass