import os

import OutsideYT


def update_combobox(combobox, items: list, def_value: str):
    combobox.clear()
    combobox.addItems(items)
    if def_value != "":
        index = list(items).index(def_value)
        combobox.setCurrentIndex(index)
    else:
        combobox.setCurrentIndex(0)
    return combobox


def find_files(args: list, folder: str, name: str = ""):
    for file in os.listdir(folder):
        if file.endswith(tuple(args)) and file.startswith(name):
            if ".txt" in args:
                with open(os.path.join(folder, file), "r", encoding="UTF-8") as f:
                    if name == "Playlist":
                        return f.read().split("\n")
                    return f.read()
            return file
    print("File not founded")
    return None
