import json
import os

import OutsideYT
from OutsideYT import app_settings_uploaders
from outside.YT_functions import download_image
from outside.functions import check_folder_name
from outside.message_boxes import error_func


def _get_download_saving_path(dialog_settings):
    if dialog_settings.Download_User_Save_Mode_radioButton.isChecked():
        user = dialog_settings.Download_Save_to_ComboBox.currentText()
        if user:
            saving_path = os.path.join(app_settings_uploaders.vids_folder, user)
        else:
            raise ValueError('User is not selected.')
    else:
        saving_path = dialog_settings.Download_Save_textBox.text()
        if not os.path.isdir(saving_path):
            raise ValueError(f'Path "{saving_path}" is not exists')
    return saving_path


def create_video_folder(table, video_info: dict, saving_path: str):
    try:
        if video_info:
            save_dir = os.path.join(saving_path, check_folder_name(video_info['title']))
            os.makedirs(os.path.join(save_dir), exist_ok=True)

            for file, key in OutsideYT.filenames_video_details.items():
                if key in video_info and video_info[key]:
                    if file.endswith(tuple(OutsideYT.json_extensions)):
                        json.dump(video_info[key],
                                  open(os.path.join(save_dir, file), 'w', encoding="UTF-8"))
                    elif file.endswith('.txt'):
                        with open(os.path.join(save_dir, file), 'w', encoding='UTF-8') as f:
                            if isinstance(video_info[key], list):
                                f.write(", ".join(video_info[key]))
                            else:
                                f.write(video_info[key])
                    elif file.endswith(tuple(OutsideYT.image_extensions)):
                        img_url = (f'https://i.ytimg.com/vi/{video_info["videoId"]}'
                                   f'/maxresdefault.jpg')
                        img = download_image(img_url)
                        if img:
                            with open(os.path.join(save_dir, file), 'wb') as f:
                                f.write(img)
            return True
    except KeyError as key:
        # error_func(f'{key} not found on video page')
        pass
    return False
