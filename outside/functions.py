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
