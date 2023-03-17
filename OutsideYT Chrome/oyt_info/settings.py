import os


class Settings:
    def __init__(self):
        self._accounts = []
        self._def_account = ""
        self._vids_folder = "videos"

    @property
    def accounts(self):
        return self._accounts

    @property
    def vids_folder(self):
        return self._vids_folder

    @property
    def def_account(self):
        return self._def_account

    def add_account(self, login):
        if self.accounts.count(login) == 0:
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

    def del_def_account(self):
        self._def_account = ""
        self.update_settings()
        return

    def create_videos_dir(self):
        path = self.vids_folder
        if not os.path.exists(path):
            os.mkdir(path)
        for login in self.accounts:
            if not os.path.exists(f'{path}/{login}'):
                os.mkdir(f'{path}/{login}')
        return

    def update_settings(self):
        with open("oyt_info/settings", "w") as file:
            file.writelines([f'accounts={",".join(self.accounts)}\n',
                             f'vids_folder={self.vids_folder}\n',
                             f'def_account={self.def_account}\n'])
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
                elif line.find("def_account") != -1:
                    self._def_account = line.split("=")[1]
                elif line.find("vids_folder") != -1:
                    self._vids_folder = line.split("=")[1]
                line = file.readline().strip()
        return

    @staticmethod
    def check_cookies():
        accs = []
        for file in os.listdir():
            if file.endswith("_cookies"):
                accs.append(file.replace("_cookies", ""))
        out = ""
        with open("oyt_info/settings", "r") as f:
            for line in f:
                if line.find("accounts=") != -1:
                    out += "accounts=" + ",".join(accs) + "\n"
                else:
                    out += line
        print(out, file=open("oyt_info/settings", "w", encoding="UTF-8"))


class AccountSettings:

    def __init__(self, account):
        self._account = account
        # self._def_access = 0
        self._def_playlist = ""
        # self._def_title = ""
        # self._def_description = ""
        # self._def_tags = []
        self._def_ends = 20
        # self._def_preview = ""
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
                             f'def_playlist={self._def_playlist}\n',
                             f'def_tags={",".join(self._def_tags)}\n',
                             f'def_ends={self._def_ends}\n',
                             f'def_preview={self._def_preview}\n',
                             f'def_access={self._def_access}\n',
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
                elif line.find("def_playlist") != -1:
                    self._def_playlist = line.split("=")[1]
                elif line.find("def_tags") != -1:
                    self._def_tags = line.split("=")[1].split(",")
                elif line.find("def_ends") != -1:
                    self._def_ends = line.split("=")
                elif line.find("def_preview") != -1:
                    self._def_preview = line.split("=")[1]
                elif line.find("def_access") != -1:
                    self._def_access = int(line.split("=")[1])
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

    def add_def_playlist(self, val):
        self._def_playlist = val
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

    def add_def_access(self, val):
        self._def_access = val
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

    @property
    def accounts(self):
        return self._accounts

    @property
    def vids_folder(self):
        return self._vids_folder

    @property
    def def_account(self):
        return self._def_account

    @property
    def def_title(self):
        return self._def_title

    @property
    def def_description(self):
        return self._def_description

    @property
    def def_playlist(self):
        return self._def_playlist

    @property
    def def_preview(self):
        return self._def_preview

    @property
    def def_tags(self):
        return self._def_tags

    @property
    def def_access(self):
        return self._def_access

    @property
    def def_ends(self):
        return self._def_ends

    @property
    def def_publ_time(self):
        return self._def_publ_time


if os.path.exists("oyt_info/settings"):
    Settings.check_cookies()
