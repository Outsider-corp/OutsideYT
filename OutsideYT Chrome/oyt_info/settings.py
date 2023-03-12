import os


class Settings:

    def __init__(self):
        self._accounts = []
        self._def_account = ""
        self._vids_folder = "videos/"
        self._def_title = ""
        self._def_description = ""
        self._def_tags = []
        self._def_ends = []
        self._def_preview = ""
        self._def_publ_time = 0
        if os.path.exists("oyt_info/settings"):
            self.read_settings("oyt_info/settings")
        self.create_videos_dir()

    def update_settings(self):
        with open("oyt_info/settings", "w") as file:
            file.writelines([f'accounts={",".join(self._accounts)}\n',
                             f'vids_folder={self._vids_folder}\n',
                             f'def_account={self._def_account}\n',
                             f'def_title={self._def_title}\n',
                             f'def_description={self._def_description}\n',
                             f'def_tags={",".join(self._def_tags)}\n',
                             f'def_ends={",".join(self._def_ends)}\n',
                             f'def_preview={self._def_preview}\n',
                             f'def_publ_time={self._def_publ_time}\n'])
        self.create_videos_dir()

    def read_settings(self, file):
        if not os.path.exists(file):
            print("Такого файла не существует")
            return
        with open(file, "r") as file:
            line = file.readline().strip()
            while line != "":
                if line.find("accounts=") != -1:
                    self._accounts = line.split("=")[1].split(",")
                elif line.find("def_title") != -1:
                    self._def_title = line.split("=")[1]
                elif line.find("def_account") != -1:
                    self._def_account = line.split("=")[1]
                elif line.find("vids_folder") != -1:
                    self._vids_folder = line.split("=")[1]
                elif line.find("def_description") != -1:
                    self._def_description = line.split("=")[1]
                elif line.find("def_tags") != -1:
                    self._def_tags = line.split("=")[1].split(",")
                elif line.find("def_ends") != -1:
                    self._def_ends = line.split("=")[1].split(",")
                elif line.find("def_preview") != -1:
                    self._def_preview = line.split("=")[1]
                elif line.find("def_publ_time") != -1:
                    self._def_publ_time = int(line.split("=")[1])
                line = file.readline().strip()
        return

    def add_account(self, login):
        if self._accounts.count(login) == 0:
            self._accounts.append(login)
            self.update_settings()
        else:
            print("Аккаунт с таким именем уже существует")
        return

    def del_account(self, login):
        self._accounts.remove(login)
        return

    def add_vids_folder(self, path):
        self._vids_folder = path
        self.update_settings()
        return

    def del_vids_folder(self):
        self._vids_folder = "/videos"
        self.update_settings()
        return

    def add_def_account(self, val):
        self._def_account = val
        self.update_settings()
        return
    def add_def_title(self, val):
        self._def_title = val
        self.update_settings()
        return

    def add_def_description(self, val):
        self._def_description = val
        self.update_settings()
        return

    def add_def_tags(self, val):
        self._def_tags = val
        self.update_settings()
        return

    def add_def_ends(self, val):
        self._def_ends = val
        self.update_settings()
        return

    def add_def_preview(self, val):
        self._def_preview = val
        self.update_settings()
        return

    def add_def_publ_time(self, val):
        self._def_publ_time = val
        self.update_settings()
        return

    def create_videos_dir(self):
        path = self._vids_folder
        if not os.path.exists(path):
            os.mkdir(path)
        for login in self._accounts:
            if not os.path.exists(f'{path}/{login}'):
                os.mkdir(f'{path}/{login}')
        return
