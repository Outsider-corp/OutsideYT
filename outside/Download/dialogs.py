from PyQt5 import QtWidgets

from outside.message_boxes import error_func


def select_saving_path(dialog_settings):
    path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                      'Select Saving folder', '.',
                                                      QtWidgets.QFileDialog.ShowDirsOnly)
    if path:
        dialog_settings.Download_Save_textBox.setText(path)


def change_saving_path():
    path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                      'Select Saving folder', '.',
                                                      QtWidgets.QFileDialog.ShowDirsOnly)
    if path:
        pass
        # app_settings_download.change_path(path)


def open_advanced_settings(parent, table):
    error_func('This action will be add later...')


