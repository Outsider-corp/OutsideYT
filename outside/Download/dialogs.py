from PyQt5 import QtWidgets

from OutsideYT import app_settings_download
from outside.message_boxes import error_func




def change_saving_path(dialog_settings):
    path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                      'Select Saving folder', '.',
                                                      QtWidgets.QFileDialog.ShowDirsOnly)
    if path:
        app_settings_download.change_path(path)
        dialog_settings.Download_SavingPath_Label.setText(app_settings_download.saving_path)


def open_advanced_settings(parent, table):
    error_func('This action will be add later...')


