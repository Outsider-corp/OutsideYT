import os

from PyQt5.QtWidgets import QWidget

from OutsideYT import foldername_forbidden_symbols


def update_combobox(combobox, items: list, def_value: str):
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
        if file.endswith(tuple(args)) and file.startswith(name.lower()):
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


def get_video_link(video_id: str):
    return f'https://youtube.com/watch?v={video_id}'


def check_folder_name(fname: str):
    for i in foldername_forbidden_symbols:
        if i in fname:
            fname = fname.replace(i, '_')
    while fname.endswith('.'):
        fname = fname[:-1]
    return fname


def change_enabled_tab_elements(dialog_settings, page_name: str, state: bool):
    current_tab = dialog_settings.OutsideYT.findChild(QWidget, f'{page_name.capitalize()}Page}')
    tab_elements = current_tab.findChildren(QWidget)

    for el in tab_elements:
        el.setEnabled(state)
    getattr(dialog_settings, f'{page_name.capitalize()}_Start').setText("Start" if state else "Stop")
    getattr(dialog_settings, f'{page_name.capitalize()}_Start').setEnabled(True)
