import os

from PyQt5.QtWidgets import QWidget

from OutsideYT import FOLDERNAME_FORBIDDEN_SYMBOLS


def update_combobox(combobox, items: list, def_value: str = ''):
    combobox.clear()
    combobox.addItems(items)
    if def_value != '':
        index = list(items).index(def_value)
        combobox.setCurrentIndex(index)
    else:
        combobox.setCurrentIndex(0)
    return combobox


def update_checkbox_select_all(checkbox, table):
    table.model()._data['Selected'] = checkbox.isChecked()
    table.update()


def find_files(args: list, folder: str, name: str = ''):
    for file in os.listdir(folder):
        if file.endswith(tuple(args)) and (file.lower().startswith(name.lower())):
            if '.txt' in args:
                with open(os.path.join(folder, file), 'r', encoding='UTF-8') as f:
                    if name.lower() == 'playlist':
                        return f.read().split('\n')
                    return f.read()
            return os.path.join(folder, file)
    print('File not founded')
    return None


def get_video_id(link: str):
    if ('/watch?v=' not in link and 'youtu.be/' not in link and 'youtube.com/embed/' not in link):
        return None
    if '/watch?v=' in link:
        video_id = link.split('/watch?v=')[1]
    elif 'youtube.com/embed/' in link:
        video_id = link.split('embed/')[1]
    else:
        video_id = link.split('youtu.be/')[1]
    if '?' in video_id:
        video_id = video_id.split('?')[0]
    if '&' in video_id:
        video_id = video_id.split('&')[0]
    return video_id


def get_video_link(video_id: str, type: str = 'full'):
    if type == 'full':
        return f'https://youtube.com/watch?v={video_id}'
    elif type == 'embed':
        return f'https://youtube.com/embed/{video_id}'
    else:
        return f'https://youtu.be/{video_id}'


def check_folder_name(fname: str):
    for i in FOLDERNAME_FORBIDDEN_SYMBOLS:
        if i in fname:
            fname = fname.replace(i, '_')
    return fname


def change_enabled_tab_elements(dialog_settings, page_name: str, state: bool,
                                block_start_button: bool = False):
    current_tab = dialog_settings.OutsideYT.findChild(QWidget, f'{page_name.capitalize()}Page')
    tab_elements = current_tab.findChildren(QWidget)

    for el in tab_elements:
        el.setEnabled(state)
    getattr(dialog_settings, f'{page_name.capitalize()}_Start').setText(
        "Start" if state else "Stop")
    if not block_start_button:
        getattr(dialog_settings, f'{page_name.capitalize()}_Start').setEnabled(True)


def calc_time_from_string(time: str):
    time_part = time.split(':')
    progress_value = int(time_part[-1]) + int(time_part[-2]) * 60
    if len(time_part) > 2:
        progress_value += int(time_part[-3]) * 3600
    return progress_value
