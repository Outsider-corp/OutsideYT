import OutsideYT


def update_download(ui, parent):
    global Download_table

    ui.Download_SavingPath_Label.setText(OutsideYT.app_settings_uploaders.vids_folder)
    ui.Download_Progress_Bar.setVisible(False)

    Download_table = ui.Download_Table

    return Download_table, ui
