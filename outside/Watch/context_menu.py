from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QMenu, QStyle

from OYT_Settings import app_settings_watchers
from outside.context_menu import add_remove_row, add_option_open_link
from outside.TableModels import remove_row


def watchers_group_dialogs_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)

    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction('Remove Row')
        remove_data.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton))
        group = table.model().get_data().loc[table.currentIndex().row(), 'Group']
        remove_data.triggered.connect(partial(remove_row, table=table,
                                              del_from_settings=partial(app_settings_watchers.del_group,
                                                                        parent=parent, group=group)))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


def watchers_dialogs_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)

    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction('Remove Row')
        remove_data.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton))
        account = table.model().get_data().loc[table.currentIndex().row(), 'Account']
        group = table.model().get_data().loc[table.currentIndex().row(), 'Group']
        remove_data.triggered.connect(partial(remove_row, table=table,
                                              del_from_settings=partial(app_settings_watchers.del_account,
                                                                        group=group,
                                                                        login=account, parent=parent)))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


def watch_context_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        if table.currentIndex().column() == 7:
            add_option_open_link(menu, table)
            menu.addSeparator()
    add_remove_row(menu, ind, table)
    cursor = QtGui.QCursor()
    menu.exec_(cursor.pos())
