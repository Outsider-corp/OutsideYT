from functools import partial

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QAbstractItemView, QMenu, QStyle

from outside.OYT_Settings import app_settings_uploaders, app_settings_download
from outside.TableModels import remove_all_rows, remove_row, remove_selected_rows
from outside.YT.functions import open_video_in_browser


def add_remove_row(menu, ind, table: QtWidgets.QAbstractItemView, type_deleting: str = ''):
    add_data = menu.addAction('Add New Row')
    add_data.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown))
    add_data.triggered.connect(lambda: table.model().insertRows())
    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction('Remove Row')
        remove_data.setIcon(
            QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton))
        remove_data.triggered.connect(
            partial(remove_row, table=table))
        table.update()
    if 'Selected' in table.model().get_data().columns and not all(
            table.model().get_data()['Selected']):
        remove_all_data = menu.addAction('Remove Unselected Rows')
        remove_all_data.setIcon(QApplication.style().standardIcon(
            QtWidgets.QStyle.SP_MessageBoxCritical))
        remove_all_data.triggered.connect(
            partial(remove_selected_rows, table=table, type_deleting=type_deleting))
    if table.model().rowCount():
        menu.addSeparator()
        del_all = menu.addAction('Clear Table')
        del_all.setIcon(QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogResetButton))
        del_all.triggered.connect(partial(remove_all_rows, table=table))


def users_dialogs_menu(pos, parent, table: QAbstractItemView, table_type: str):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction('Remove Row')
        remove_data.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton))
        acc = table.model().get_data().loc[ind.row(), 'Account']
        del_func = app_settings_uploaders.del_account if table_type == 'upload' else \
            app_settings_download.del_account
        remove_data.triggered.connect(partial(remove_row, table=table,
                                              del_from_settings=partial(del_func,
                                                                        parent=parent, login=acc)))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())


def add_option_open_link(menu, table: QAbstractItemView):
    """
    Adding function for table context menu: open url in browser
    """

    url = table.model().get_data().loc[table.currentIndex().row(), "Link"]
    open_video = menu.addAction("Open video")
    open_video.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))
    open_video.triggered.connect(partial(open_video_in_browser, url))