import os


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
    if 'youtube.com/watch' not in link and 'youtu.be/' not in link:
        return None
    if 'youtube.com/watch' in link:
        video_id = link.split('/watch?v=')[1]
    else:
        video_id = link.split('youtu.be/')[1]
    if '?' in video_id:
        video_id = video_id.split('?')[0]
    if '&' in video_id:
        video_id = video_id.split('&')[0]
    return video_id
