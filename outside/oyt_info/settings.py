import json
import os

from outside.message_boxes import error_func, warning_func


class SettingsUploaders:
    def __init__(self, file) -> None:
        self._accounts = {}
        self._def_account = ''
        self._vids_folder = 'videos'
        self.file = file
        if file:
            self.read_settings()
            self.check_cookies()

    def __str__(self) -> str:
        return 'uploaders'

    @property
    def accounts(self):
        return self._accounts

    @property
    def vids_folder(self):
        return self._vids_folder

    @property
    def def_account(self):
        return self._def_account

    def add_account(self, acc: dict, **kwargs):
        if list(acc.keys())[0] not in self.accounts:
            self._accounts.update(acc)
            self.update_settings()
        else:
            error_func('Аккаунт с таким именем уже существует')

    def del_account(self, login, parent=None, **kwargs):
        if login in self.accounts and warning_func(
                f"Are you sure you want to delete account '{login}' ({self.accounts[login]})",
                parent):
            self._accounts.pop(login)
            if self.def_account == login:
                self.del_def_account()
            os.remove(os.path.join(os.path.dirname(self.file), self.__str__(), f'{login}_cookies'))
            self.update_settings()

    def edit_account(self, old_name: str, new_name: str):
        if new_name in self.accounts:
            error_func(f"Account name '{new_name}' is already used.")
            return
        if old_name != new_name:
            self._accounts[new_name] = self.accounts[old_name]
            del self._accounts[old_name]
            if self.def_account == old_name:
                self._def_account = new_name
            os.rename(os.path.join(os.path.dirname(self.file), 'uploaders', f'{old_name}_cookies'),
                      os.path.join(os.path.dirname(self.file), 'uploaders', f'{new_name}_cookies'))
            self.update_settings()

    def find_account(self, login: str) -> bool:
        return login in self.accounts

    def update_accounts(self, accs: dict):
        self._accounts = accs
        self.update_settings()

    def add_vids_folder(self, path: str):
        self._vids_folder = path
        self.update_settings()

    def del_vids_folder(self):
        self._vids_folder = 'videos'
        self.update_settings()

    def add_def_account(self, login: str):
        self._def_account = login
        self.update_settings()

    def del_def_account(self):
        self._def_account = ''
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
            data = {'accs': self.accounts, 'def_acc': self.def_account,
                    'vids_folder': self.vids_folder}
            json.dump(data, f)
        self.create_videos_dir()

    def read_settings(self):
        if not os.path.exists(self.file):
            self.update_settings()
            return
        with open(self.file, 'r') as file:
            data = json.load(file)
            self._accounts = data['accs']
            self._def_account = data['def_acc'] if data['def_acc'] in self.accounts else ''
            self._vids_folder = data['vids_folder']
        return

    def check_cookies(self):
        folder = os.path.dirname(self.file)
        os.makedirs(os.path.join(folder, self.__str__()), exist_ok=True)
        to_del = [acc for acc in self.accounts if not os.path.isfile(
            os.path.join(folder, self.__str__(), f'{acc}_cookies'))]
        for acc in to_del:
            self._accounts.pop(acc)
        if not os.path.isfile(os.path.join(folder, self.__str__(), f'{self.def_account}_cookies')):
            self.del_def_account()
        else:
            self.update_settings()


class SettingsWatchers:

    def __init__(self, file: str) -> None:
        self._groups = {'No group': {}}
        self._def_group = 'No group'
        self.file = file
        if file:
            self.read_settings()
            self.check_cookies()

    def __str__(self) -> str:
        return 'watchers'

    @property
    def accounts(self):
        all_accs = {}
        for accs in self.groups.values():
            all_accs.update(accs)
        return all_accs

    @property
    def groups(self):
        return self._groups

    @property
    def def_group(self):
        return self._def_group

    def add_group(self, group: str, error_ignore: bool = False):
        if group not in self.groups:
            self._groups[group] = {}
            self.update_settings()
            return True
        if not error_ignore:
            error_func(f"Группа с таким названием уже существует - '{group}'")
        return False

    def add_account(self, acc: dict, group: str = '', **kwargs):
        if not group:
            group = self.def_group
        if list(acc.keys())[0] not in self.accounts:
            self._groups[group].update(acc)
            self.update_settings()
        else:
            error_func(f"Аккаунт с таким именем уже существует в группе '{group}': '{acc}'")

    def edit_account(self, group, old_name, new_group=None, new_name=None):
        name = old_name
        if group not in self.groups:
            for key in self.groups:
                if old_name in self.groups[key]:
                    group = key
                    break
        if old_name != new_name and new_name not in self.accounts:
            self._groups[group][new_name] = self.groups[group][old_name]
            del self._groups[group][old_name]
            os.rename(
                os.path.join(os.path.dirname(self.file), self.__str__(), f'{old_name}_cookies'),
                os.path.join(os.path.dirname(self.file), self.__str__(), f'{new_name}_cookies'))
            name = new_name
        if group != new_group and new_group in self.groups:
            self._groups[new_group][name] = self.groups[group][name]
            del self._groups[group][name]
        self.update_settings()

    def del_account(self, group: str, login: str, parent=None):
        if group in self.groups and login in self.groups[group] and warning_func(
                f"Are you sure you want to delete account '{login}'"
                f", group '{group}' ({self.groups[group][login]})", parent):
            self._groups[group].pop(login)
            os.remove(os.path.join(os.path.dirname(self.file), self.__str__(), f'{login}_cookies'))
            self.update_settings()

    def del_group(self, group: str, parent=None):
        if warning_func(f"Are you sure you want to delete group '{group}'?", parent):
            if group == 'No group':
                return
        if group == self.def_group:
            self.del_def_group()
        for acc, mail in self.groups[group].items():
            self._groups[self.def_group].update({acc: mail})
        self._groups.pop(group)
        self.update_settings()
        return

    def find_account(self, login):
        return any(login in group for group in self.groups.values())

    def update_groups(self, groups: dict):
        for g, accs in groups.items():
            self._groups[g] = accs
        self.update_settings()

    def _update_accounts_in_group(self, group: str, accs: dict):
        self._groups[group] = accs
        self.update_settings()

    def change_group_name(self, old_name: str, new_name: str):
        if new_name not in self.groups:
            self._groups[new_name] = self.groups[old_name]
            if old_name == 'No group':
                self._groups[old_name] = {}
            else:
                del self._groups[old_name]
                if old_name == self.def_group:
                    self.add_def_group(new_name)
            self.update_settings()
        else:
            error_func('Группа с таким именем уже существует!')

    def add_def_group(self, group):
        if group in self.groups:
            self._def_group = group
            self.update_settings()

    def del_def_group(self):
        self._def_group = 'No group'
        self.update_settings()

    def update_settings(self):
        with open(self.file, 'w') as f:
            data = {}
            data['groups'] = self.groups
            data['def_group'] = self.def_group
            json.dump(data, f)

    def read_settings(self):
        if not os.path.exists(self.file):
            self.update_settings()
            return
        with open(self.file, 'r', encoding='UTF-8') as file:
            data = json.load(file)
            if 'No group' not in data['groups']:
                self._groups = {'No group': {}}
            self._groups.update(data['groups'])
            self._def_group = data['def_group'] if data['def_group'] else 'No group'
        return

    def check_cookies(self):
        folder = os.path.dirname(self.file)
        os.makedirs(os.path.join(folder, 'watchers'), exist_ok=True)
        to_del = []
        for group_name, group in self.groups.items():
            for acc_name in group:
                if not os.path.isfile(os.path.join(folder, 'watchers', f'{acc_name}_cookies')):
                    to_del.append((group_name, acc_name))  # noqa: PERF401
        for acc in to_del:
            self._groups[acc[0]].pop(acc[1])
        # for group_name, group in self.groups.items():
        #     if len(group) == 0:
        #         to_del.append(group_name)
        # for group in to_del:
        #     self._groups.pop(group)
        if self.def_group not in self.groups:
            self.del_def_group()
        self.update_settings()

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
