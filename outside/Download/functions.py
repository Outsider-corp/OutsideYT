import json
import os
from typing import List

from outside.OYT_Settings import FILENAMES_VIDEO_DETAILS, JSON_EXTENSIONS, IMAGE_EXTENSIONS
from outside.OYT_Settings import app_settings_uploaders
from outside.YT.download_model import OutsideDownloadVideoYT
from outside.YT.functions import download_image
from outside.exceptions import NoAvailableQualityError
from outside.functions import check_folder_name, get_video_link
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


def create_video_folder(video_info: dict, saving_path: str):
    try:
        if video_info:
            save_dir = os.path.join(saving_path, check_folder_name(video_info['title']))
            os.makedirs(os.path.join(save_dir), exist_ok=True)
            for file, key in FILENAMES_VIDEO_DETAILS.items():
                if key in video_info and video_info[key]:
                    if file.endswith(tuple(JSON_EXTENSIONS)):
                        json.dump(video_info[key],
                                  open(os.path.join(save_dir, file), 'w', encoding="UTF-8"))
                    elif file.endswith('.txt'):
                        with open(os.path.join(save_dir, file), 'w', encoding='UTF-8') as f:
                            if isinstance(video_info[key], list):
                                f.write(",".join(video_info[key]))
                            else:
                                f.write(video_info[key])
                    elif file.endswith(tuple(IMAGE_EXTENSIONS)):
                        img_url = (f'https://i.ytimg.com/vi/{video_info["videoId"]}'
                                   f'/maxresdefault.jpg')
                        download_image(img_url, path=os.path.join(save_dir, file))
            return True
    except KeyError as key:
        error_func(f'{key} not found on video page')
        pass
    return False


def start_video_download(videos: List, saving_path: str, completed_tasks_info: List,
                         params: dict, thread):
    cnt_videos = len([1 for vid in videos if vid['Selected']])
    i = 1
    for num, video in enumerate(videos):
        if video['Selected']:
            try:
                thread.update_progress_info(label_text=f"{i}/{cnt_videos} - {video['Video']}")
                i += 1
                saving_path_video = os.path.join(saving_path, check_folder_name(video['Video']))
                os.makedirs(saving_path_video, exist_ok=True)
                video_down = OutsideDownloadVideoYT(get_video_link(video['Link'], 'embed'),
                                                    video_info=video['_download_info'],
                                                    params=params,
                                                    callback_func=thread.update_progress_bar,
                                                    callback_err=thread.show_error,
                                                    _stop=thread.stop)
                if video_down.download_video(saving_path=saving_path_video):
                    completed_tasks_info[num] = False
                if thread.stop():
                    break
            except NoAvailableQualityError:
                thread.show_error("Can't find any settings that meet the selected parameters")
            except Exception as e:
                print(f'Error on start downloading...\n{e}')


def save_videos_info(videos, saving_path: str, completed_tasks_info: List, thread):
    cnt_videos = len(videos)
    for num, video in enumerate(videos):
        if thread.stop_signal:
            return
        if video['Selected']:
            if create_video_folder(video_info=video['_download_info'], saving_path=saving_path):
                thread.update_progress_bar(int((num + 1) / cnt_videos * 100))
                completed_tasks_info[num] = False
