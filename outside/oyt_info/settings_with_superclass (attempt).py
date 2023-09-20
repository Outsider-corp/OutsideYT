import json
import os


class SettingsAccounts:
    def __init__(self, file) -> None:
        self._accounts = {}
        self._def_account = ''
        self.file = file
        if file:
            self.read_settings()
            self.check_cookies()

    @property
    def accounts(self):
        return self._accounts

    @property
    def def_account(self):
        return self._def_account

    def add_account(self, acc: dict):
        if list(acc.keys())[0] not in self.accounts:
            self._accounts.update(acc)
            self.update_settings()
        else:
            print('Аккаунт с таким именем уже существует')

    def del_account(self, login):
        self._accounts.pop(login)
        self.update_settings()

    def update_accounts(self, accs):
        self._accounts = accs
        self.update_settings()

    def add_def_account(self, login):
        self._def_account = login
        self.update_settings()

    def del_def_account(self):
        self._def_account = ''
        self.update_settings()

    def update_settings(self):
        with open(self.file, 'w') as f:
            data = {}
            data['accs'] = self.accounts
            data['def_acc'] = self.def_account
            json.dump(data, f)

    def read_settings(self):
        if not os.path.exists(self.file):
            self.update_settings()
            return
        with open(self.file, 'r') as file:
            data = json.load(file)
            self._accounts = data['accs']
            self._def_account = data['def_acc']
        return

    def check_cookies(self):
        folder = os.path.dirname(self.file)
        to_del = []
        os.makedirs(os.path.join(folder, 'uploaders'), exist_ok=True)
        for acc in self.accounts:
            if not os.path.isfile(os.path.join(folder, 'uploaders', f'{acc}_cookies')):
                to_del.append(acc)
        for acc in to_del:
            self._accounts.pop(acc)
        if not os.path.isfile(os.path.join(folder, 'uploaders', f'{self.def_account}_cookies')):
            self.del_def_account()
        else:
            self.update_settings()


class SettingsUploaders(SettingsAccounts):
    def __init__(self, file) -> None:
        super().__init__(file)
        self._vids_folder = 'videos'

    @property
    def vids_folder(self):
        return self._vids_folder

    def add_vids_folder(self, path):
        self._vids_folder = path
        self.update_settings()

    def del_vids_folder(self):
        self._vids_folder = 'videos'
        self.update_settings()

    def create_videos_dir(self):
        path = self.vids_folder
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        for login in self.accounts:
            if not os.path.exists(os.path.join(path, login)):
                os.mkdir(os.path.join(path, login))

    def update_settings(self):
        with open(self.file, 'w') as f:
            data = {}
            data['accs'] = self.accounts
            data['def_acc'] = self.def_account
            data['vids_folder'] = self.vids_folder
            json.dump(data, f)
        self.create_videos_dir()

    def read_settings(self):
        if not os.path.exists(self.file):
            self.update_settings()
            return
        with open(self.file, 'r') as file:
            data = json.load(file)
            self._accounts = data['accs']
            self._def_account = data['def_acc']
            self._vids_folder = data['vids_folder']
        return


class SettingsWatchers(SettingsAccounts):
    def __init__(self, file) -> None:
        super().__init__(file)








# class AccountSettings:
#
#     def __init__(self, account):
#         self._account = account
#         # self._def_access = 0
#         self._def_playlist = ""
#         # self._def_title = ""
#         # self._def_description = ""
#         # self._def_tags = []
#         self._def_ends = 20
#         # self._def_preview = ""
#         self._def_publ_time = 0
#         if os.path.exists("oyt_info/settings"):
#             self.read_settings("oyt_info/settings")
#         self.create_videos_dir()
#
#     def update_settings(self):
#         with open("oyt_info/settings", "w") as file:
#             file.writelines([f'accounts={",".join(self._accounts)}\n',
#                              f'vids_folder={self._vids_folder}\n',
#                              f'def_account={self._def_account}\n',
#                              f'def_title={self._def_title}\n',
#                              f'def_description={self._def_description}\n',
#                              f'def_playlist={self._def_playlist}\n',
#                              f'def_tags={",".join(self._def_tags)}\n',
#                              f'def_ends={self._def_ends}\n',
#                              f'def_preview={self._def_preview}\n',
#                              f'def_access={self._def_access}\n',
#                              f'def_publ_time={self._def_publ_time}\n'])
#         self.create_videos_dir()
#
#     def read_settings(self, file):
#         if not os.path.exists(file):
#             print("Такого файла не существует")
#             return
#         with open(file, "r") as file:
#             line = file.readline().strip()
#             while line != "":
#                 if line.find("accounts=") != -1:
#                     self._accounts = line.split("=")[1].split(",")
#                 elif line.find("def_title") != -1:
#                     self._def_title = line.split("=")[1]
#                 elif line.find("def_account") != -1:
#                     self._def_account = line.split("=")[1]
#                 elif line.find("vids_folder") != -1:
#                     self._vids_folder = line.split("=")[1]
#                 elif line.find("def_description") != -1:
#                     self._def_description = line.split("=")[1]
#                 elif line.find("def_playlist") != -1:
#                     self._def_playlist = line.split("=")[1]
#                 elif line.find("def_tags") != -1:
#                     self._def_tags = line.split("=")[1].split(",")
#                 elif line.find("def_ends") != -1:
#                     self._def_ends = line.split("=")
#                 elif line.find("def_preview") != -1:
#                     self._def_preview = line.split("=")[1]
#                 elif line.find("def_access") != -1:
#                     self._def_access = int(line.split("=")[1])
#                 elif line.find("def_publ_time") != -1:
#                     self._def_publ_time = int(line.split("=")[1])
#                 line = file.readline().strip()
#         return
#
#     def add_account(self, login):
#         if self._accounts.count(login) == 0:
#             self._accounts.append(login)
#             self.update_settings()
#         else:
#             print("Аккаунт с таким именем уже существует")
#         return
#
#     def del_account(self, login):
#         self._accounts.remove(login)
#         return
#
#     def add_vids_folder(self, path):
#         self._vids_folder = path
#         self.update_settings()
#         return
#
#     def del_vids_folder(self):
#         self._vids_folder = "/videos"
#         self.update_settings()
#         return
#
#     def add_def_account(self, val):
#         self._def_account = val
#         self.update_settings()
#         return
#
#     def add_def_title(self, val):
#         self._def_title = val
#         self.update_settings()
#         return
#
#     def add_def_description(self, val):
#         self._def_description = val
#         self.update_settings()
#         return
#
#     def add_def_playlist(self, val):
#         self._def_playlist = val
#         self.update_settings()
#         return
#
#     def add_def_tags(self, val):
#         self._def_tags = val
#         self.update_settings()
#         return
#
#     def add_def_ends(self, val):
#         self._def_ends = val
#         self.update_settings()
#         return
#
#     def add_def_preview(self, val):
#         self._def_preview = val
#         self.update_settings()
#         return
#
#     def add_def_access(self, val):
#         self._def_access = val
#         self.update_settings()
#         return
#
#     def add_def_publ_time(self, val):
#         self._def_publ_time = val
#         self.update_settings()
#         return
#
#     def create_videos_dir(self):
#         path = self._vids_folder
#         if not os.path.exists(path):
#             os.mkdir(path)
#         for login in self._accounts:
#             if not os.path.exists(f'{path}/{login}'):
#                 os.mkdir(f'{path}/{login}')
#         return
#
#     @property
#     def accounts(self):
#         return self._accounts
#
#     @property
#     def vids_folder(self):
#         return self._vids_folder
#
#     @property
#     def def_account(self):
#         return self._def_account
#
#     @property
#     def def_title(self):
#         return self._def_title
#
#     @property
#     def def_description(self):
#         return self._def_description
#
#     @property
#     def def_playlist(self):
#         return self._def_playlist
#
#     @property
#     def def_preview(self):
#         return self._def_preview
#
#     @property
#     def def_tags(self):
#         return self._def_tags
#
#     @property
#     def def_access(self):
#         return self._def_access
#
#     @property
#     def def_ends(self):
#         return self._def_ends
#
#     @property
#     def def_publ_time(self):
#         return self._def_publ_time

