import json
import os

import outside.video_qualities
from outside.message_boxes import error_func, warning_func


class AppSettings:
    """Settings for OutsideYT."""


class SettingsUsers(AppSettings):
    def __init__(self, file, videos_folder='videos', settings_type='upload',
                 cookies_folder='outside/oyt_info') -> None:
        self._accounts = {}
        self._def_account = ''
        self._vids_folder = videos_folder
        self.settings_type = settings_type
        self.cookies_folder = os.path.join(cookies_folder, self.__str__())
        self.file = file
        if file:
            self.read_settings()
            self.check_cookies()

    def __str__(self) -> str:
        return self.settings_type

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

    def del_account(self, login, parent=None, confirm: bool = False, **kwargs):
        if login in self.accounts:
            if confirm or warning_func(
                    f"Are you sure you want to delete account '{login}' ({self.accounts[login]})",
                    parent):
                self._accounts.pop(login)
                if self.def_account == login:
                    self.del_def_account()
                os.remove(os.path.join(self.cookies_folder, f'{login}_cookies'))
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
            os.rename(
                os.path.join(self.cookies_folder, f'{old_name}_cookies'),
                os.path.join(self.cookies_folder, f'{new_name}_cookies'))
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
        os.makedirs(self.cookies_folder, exist_ok=True)
        to_del = [acc for acc in self.accounts if not os.path.isfile(
            os.path.join(self.cookies_folder, f'{acc}_cookies'))]
        for acc in to_del:
            self._accounts.pop(acc)
        if not os.path.isfile(os.path.join(self.cookies_folder, f'{self.def_account}_cookies')):
            self.del_def_account()
        else:
            self.update_settings()


class SettingsWatchers(AppSettings):

    def __init__(self, file: str, cookies_folder='outside/oyt_info') -> None:
        self._groups = {'No group': {}}
        self._def_group = 'No group'
        self.file = file
        self.cookies_folder = os.path.join(cookies_folder, self.__str__())
        if file:
            self.read_settings()
            self.check_cookies()

    def __str__(self) -> str:
        return 'watch'

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
                os.path.join(self.cookies_folder, f'{old_name}_cookies'),
                os.path.join(self.cookies_folder, f'{new_name}_cookies'))
            name = new_name
        if group != new_group and new_group in self.groups:
            self._groups[new_group][name] = self.groups[group][name]
            del self._groups[group][name]
        self.update_settings()

    def del_account(self, login: str, group: str = None, parent=None, confirm: bool = False):
        group = group or self.find_group(login)
        if group:
            if confirm or warning_func(f"Are you sure you want to delete account '{login}'"
                                       f", group '{group}' ({self.groups[group][login]})", parent):
                self._groups[group].pop(login)
                os.remove(os.path.join(self.cookies_folder, f'{login}_cookies'))
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

    def find_group(self, login):
        for group_name, group in self.groups.items():
            if login in group:
                return group_name
        return None

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
        os.makedirs(self.cookies_folder, exist_ok=True)
        to_del = []
        for group_name, group in self.groups.items():
            for acc_name in group:
                if not os.path.isfile(os.path.join(self.cookies_folder, f'{acc_name}_cookies')):
                    to_del.append((group_name, acc_name))
        for acc in to_del:
            self._groups[acc[0]].pop(acc[1])
        if self.def_group not in self.groups:
            self.del_def_group()
        self.update_settings()


class SettingsDownloads:
    def __init__(self, file: str):
        self.file = file
        self.ext = 'Any'
        self.prefer = outside.video_qualities.DEFAULT_PREFER_QUALITY
        self.simple_quality_video = 'Any'
        self.quality_video = 'Any'
        self.quality_audio = 'Any'
        self.simple_download = True
        self.download_type = 'full'
        self.if_exists = outside.video_qualities.IF_EXISTS_DEFAULT
        if os.path.exists(file):
            self.read_settings()
        else:
            self.update_settings()

    def change_settings(self, **kwargs):
        """
        Change settings.
        Args:
            kwargs: dict - dict with new values of settings. Available keys:
            quality_video: str, quality_audio: str, ext: str, prefer: str, simple_download: bool,
            download_type: str, simple_quality_video: str, if_exists: str
        """
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)
        self.update_settings()

    def export_settings_as_dict(self):
        params = {'simple': self.simple_download,
                  'video': {
                      'video_quality': self.simple_quality_video if (
                          self.simple_download) else self.quality_video,
                      'video_ext': self.ext
                  },
                  'audio': {
                      'audio_quality': self.quality_audio,
                      'audio_ext': self.ext
                  },
                  'prefer': self.prefer,
                  'download_type': self.download_type,
                  'if_exists': self.if_exists
                  }
        return params

    def update_settings(self):
        with open(self.file, 'w', encoding='utf-8') as f:
            settings = {'quality_video': self.quality_video,
                        'quality_audio': self.quality_audio,
                        'simple_quality_video': self.simple_quality_video,
                        'ext': self.ext,
                        'prefer': self.prefer,
                        'simple_download': self.simple_download,
                        'download_type': self.download_type,
                        'if_exists': self.if_exists}
            json.dump(settings, f)

    def read_settings(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        self.simple_quality_video = settings['simple_quality_video']
        self.ext = settings['ext']
        self.prefer = settings['prefer']
        self.quality_video = settings['quality_video']
        self.quality_audio = settings['quality_audio']
        self.simple_download = settings['simple_download']
        self.download_type = settings['download_type']
        self.if_exists = settings['if_exists']
