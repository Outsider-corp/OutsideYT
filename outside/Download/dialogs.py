from functools import partial

from PyQt5 import QtWidgets

from OutsideYT import app_settings_download
from outside.video_qualities import VIDEO_EXTS, VIDEO_QUALITIES, SIMPLE_VIDEO_QUALITIES, \
    AUDIO_QUALITIES, PREFER_QUALITY, IF_EXISTS_VARS
from outside.functions import update_combobox
from outside.views_py import DownloadAdvancedSettings_Dialog


def select_saving_path(dialog_settings):
    path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                      'Select Saving folder', '.',
                                                      QtWidgets.QFileDialog.ShowDirsOnly)
    if path:
        dialog_settings.Download_Save_textBox.setText(path)


def open_advanced_settings(parent):
    def ok():
        changes_all = {
            'quality_video': ds.Video_quality_comboBox.currentText(),
            'quality_audio': ds.Audio_quality_comboBox.currentText(),
            'simple_quality_video': ds.Video_quality_comboBox.currentText(),
            'ext': ds.Extensions_comboBox.currentText(),
            'prefer': ds.Prefer_quality_comboBox.currentText(),
            'simple_download': ds.Simple_download_checkBox.isChecked(),
            'if_exists': ds.If_exists_comboBox.currentText()
        }
        if ds.Audio_radioButton.isChecked():
            changes = {'download_type': 'audio'}
            changes.update({key: val for key, val in changes_all.items() if key in ['quality_audio',
                                                                                    'ext',
                                                                                    'prefer']})
        elif ds.Video_radioButton.isChecked():
            changes = {'download_type': 'video'}
            changes.update({key: val for key, val in changes_all.items() if key in ['quality_video',
                                                                                    'ext',
                                                                                    'prefer']})
        else:
            changes = {'download_type': 'full'}
            changes.update(changes_all)
            if changes['simple_download']:
                del changes['quality_video']
            else:
                del changes['simple_quality_video']

        app_settings_download.change_settings(**changes)
        dialog.accept()

    dialog = QtWidgets.QDialog(parent)
    dialog.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    ds = DownloadAdvancedSettings_Dialog.Ui_DownloadSettings_Dialog()
    ds.setupUi(dialog)
    ds.Prefer_quality_comboBox = update_combobox(ds.Prefer_quality_comboBox,
                                                 items=PREFER_QUALITY,
                                                 def_value=app_settings_download.prefer)

    ds.Extensions_comboBox = update_combobox(ds.Extensions_comboBox,
                                             items=['Any'] + VIDEO_EXTS,
                                             def_value=app_settings_download.ext)

    ds.If_exists_comboBox = update_combobox(ds.If_exists_comboBox,
                                            items=IF_EXISTS_VARS,
                                            def_value=app_settings_download.if_exists)

    ds.Simple_download_checkBox.setChecked(app_settings_download.simple_download)
    _change_sort_combos(ds)

    if app_settings_download.download_type == 'audio':
        ds.Audio_radioButton.setChecked(True)
        _download_type(ds, 'audio')
    elif app_settings_download.download_type == 'video':
        ds.Video_radioButton.setChecked(True)
        _download_type(ds, 'video')
    else:
        ds.Full_video_radioButton.setChecked(True)
        _download_type(ds, 'full')

    ds.Audio_radioButton.clicked.connect(partial(_download_type, ds=ds, state='audio'))
    ds.Video_radioButton.clicked.connect(partial(_download_type, ds=ds, state='video'))
    ds.Full_video_radioButton.clicked.connect(partial(_download_type, ds=ds, state='full'))
    ds.Simple_download_checkBox.clicked.connect(partial(_change_sort_combos, ds=ds))
    ds.Prefer_quality_comboBox.currentIndexChanged.connect(partial(_change_sort_combos, ds=ds))

    ds.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(ok)
    ds.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(dialog.reject)
    dialog.exec_()


def _download_type(ds: DownloadAdvancedSettings_Dialog.Ui_DownloadSettings_Dialog, state: str):
    if state == 'full':
        ds.Audio_quality_comboBox.setEnabled(True)
        ds.Video_quality_comboBox.setEnabled(True)
        ds.Simple_download_checkBox.setVisible(True)
    else:
        set_state = state == 'video'
        ds.Audio_quality_comboBox.setEnabled(not set_state)
        ds.Video_quality_comboBox.setEnabled(set_state)
        ds.Simple_download_checkBox.setVisible(False)


def _change_sort_combos(ds: DownloadAdvancedSettings_Dialog.Ui_DownloadSettings_Dialog):
    if ds.Simple_download_checkBox.isChecked():
        video_list = SIMPLE_VIDEO_QUALITIES
        def_val = app_settings_download.simple_quality_video
    else:
        video_list = VIDEO_QUALITIES
        def_val = app_settings_download.quality_video
    if ds.Prefer_quality_comboBox.currentText().lower() == 'worse':
        video_list = video_list[::-1]
        audio_list = AUDIO_QUALITIES[::-1]
    else:
        audio_list = AUDIO_QUALITIES
    ds.Audio_quality_comboBox = update_combobox(ds.Audio_quality_comboBox,
                                                items=['Any'] + audio_list,
                                                def_value=app_settings_download.quality_audio)
    ds.Video_quality_comboBox = update_combobox(ds.Video_quality_comboBox,
                                                items=['Any'] + video_list,
                                                def_value=def_val)
