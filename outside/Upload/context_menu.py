import os
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QMenu, QStyle

import OutsideYT
from outside.context_menu import add_remove_row
from outside.message_boxes import error_func
from outside.TableModels import remove_row
from outside.Upload import dialogs
from outside.Upload.TableModels import UploadModel, open_location


def upload_context_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        if table.currentIndex().column() == 4:
            set_time = menu.addAction('Set Publish Time')
            set_time.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            set_time.triggered.connect(
                partial(dialogs.set_upload_time_for_video, parent=parent, table=table,
                        video_id=table.currentIndex().row()))
            if table.model().get_data().at[table.currentIndex().row(), 'Publish'] != 'Now':
                remove_time = menu.addAction('Remove Publish Time')
                remove_time.setIcon(QApplication.style().standardIcon(QStyle.SP_BrowserReload))

                def remove_time_func():
                    table.model()._data.at[table.currentIndex().row(), 'Publish'] = 'Now'
                    table.update()

                remove_time.triggered.connect(remove_time_func)
        elif table.currentIndex().column() == 5:
            path = table.model().get_data().at[table.currentIndex().row(), 'Video']
            if path not in ['', UploadModel.default_content['Video']]:
                start_video = menu.addAction('Start Video in Player')
                open_video_folder = menu.addAction('Open Video folder')
                open_video_folder.setIcon(QApplication.style().standardIcon(QStyle.SP_FileIcon))
                start_video.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))

                def open_folder():
                    fpath = os.path.dirname(path)
                    if os.path.exists(fpath):
                        os.startfile(fpath)
                    else:
                        error_func('Path not found.')

                def play():
                    if os.path.exists(path):
                        os.startfile(path)
                    else:
                        error_func('File not found.')

                open_video_folder.triggered.connect(open_folder)
                start_video.triggered.connect(play)
                menu.addSeparator()
            select_video = menu.addAction('Select Video')
            select_video.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            select_video.triggered.connect(
                partial(open_location, table=table, index=table.currentIndex().row(), ext='Video'))
        elif table.currentIndex().column() == 8:
            path = table.model().get_data().at[table.currentIndex().row(), 'Preview']
            if path not in ['', UploadModel.default_content['Preview']]:
                start_video = menu.addAction('Show Preview')
                open_video_folder = menu.addAction('Open Preview folder')
                open_video_folder.setIcon(QApplication.style().standardIcon(QStyle.SP_FileIcon))
                start_video.setIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon))

                def open_folder():
                    fpath = os.path.dirname(path)
                    if os.path.exists(fpath):
                        os.startfile(fpath)
                    else:
                        error_func('Path not found.')

                def play():
                    if os.path.exists(path):
                        os.startfile(path)
                    else:
                        error_func('File not found.')

                open_video_folder.triggered.connect(open_folder)
                start_video.triggered.connect(play)
                menu.addSeparator()
            select_video = menu.addAction('Select Preview')
            select_video.setIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            select_video.triggered.connect(
                partial(open_location, table=table, index=table.currentIndex().row(), ext='Preview'))
        menu.addSeparator()
    add_remove_row(menu, ind, table, None)
    cursor = QtGui.QCursor()
    menu.exec_(cursor.pos())


def uploaders_dialogs_menu(pos, parent, table: QAbstractItemView):
    menu = QMenu(parent)
    ind = table.indexAt(pos)
    if ind.isValid() and table.selectedIndexes():
        remove_data = menu.addAction('Remove Row')
        remove_data.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton))
        acc = table.model().get_data().loc[ind.row(), 'Account']
        remove_data.triggered.connect(partial(remove_row, table=table,
                                              del_from_settings=partial(OutsideYT.app_settings_uploaders.del_account,
                                                                        parent=parent, login=acc)))
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())
