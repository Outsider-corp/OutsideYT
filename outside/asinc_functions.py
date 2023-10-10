import asyncio
import os

from typing import List
import aiohttp
from PyQt5.QtCore import QMutex, QThread, pyqtSignal, QObject, QThreadPool
from PyQt5.QtWidgets import QTableView

import OutsideYT
from outside.Download.functions import create_video_folder
from outside.YT.functions import get_video_info, watching
from outside.YT.download_model import OutsideDownloadVideoYT
from outside.functions import check_folder_name, get_video_link


class ProgressMutex:
    def __init__(self, total_steps: int, progress_bar) -> None:
        self.mutex = QMutex()
        self.progress = 0
        self.total_steps = total_steps
        self.progress_bar = progress_bar

    def inc(self):
        self.mutex.lock()
        self.progress += 1
        self.progress_bar.setValue(self.progress)
        self.mutex.unlock()


class WorkerManager(QObject):
    def __init__(self, threads_list, dialog_settings) -> None:
        super(WorkerManager, self).__init__()
        self.threadpool = QThreadPool()
        self.dialog_settings = dialog_settings

    def run(self):
        while self.threads_list:
            pass


class WatchThread(QThread):

    def __init__(self, table, table_row: int, driver_headless=True, parent=None,
                 offsets: List = None) -> None:
        super().__init__(parent)
        self._table = table
        self._video = get_video_link(table.model().get_data().loc[table_row, "Link"], type='embed')
        self._durations = table.model().get_data().loc[table_row, "Duration"]
        self._users = list(OutsideYT.app_settings_watchers.groups[
                               table.model().get_data().loc[table_row, "Watchers Group"]].keys())
        self._progress_bar_num = table_row
        self._lock = asyncio.Lock()
        sum_offsets = sum(offsets) if offsets else 0
        self._total_steps = len(self._users) * self._durations + sum_offsets
        self._progress = 0
        self.driver_headless = driver_headless
        self._offsets = offsets
        self.update_progress_signal = pyqtSignal(int)

    async def progress_bar_inc(self):
        async with self._lock:
            self._progress += 1
            new_val = int(self._progress / self._total_steps * 100)
            self.update_progress_signal.emit(new_val)

    async def start_loop(self):
        atasks = [watching(self._video, self._durations, user,
                           driver_headless=self.driver_headless,
                           progress_inc=self.progress_bar_inc)
                  for user in self._users]
        await asyncio.gather(*atasks)

    def run(self):
        asyncio.run(self.start_loop())
        self.update_progress_signal.emit()


class GetVideoInfoThread(QThread):
    update_progress_signal = pyqtSignal(int)
    update_progress_label_signal = pyqtSignal(str)

    def __init__(self, tasks: list, progress_bar=None, progress_label=None,
                 parent=None, additional_args: list = None, **kwargs) -> None:
        super().__init__(parent)
        self.tasks = tasks
        self.results = []
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.lock = asyncio.Lock()
        self.total_steps = len(tasks)
        self.progress = 0
        self._add_args = additional_args if additional_args else []
        self.semaphore = asyncio.Semaphore(OutsideYT.ASYNC_LIMIT)

    def update_progress_info(self, label_text: str = None, bar_value: int = 0):
        self.update_progress_label_signal.emit(label_text)
        self.update_progress_signal.emit(bar_value)

    async def progress_bar_inc(self):
        async with self.lock:
            if self.progress_bar:
                self.progress += 1
                new_val = int(self.progress / self.total_steps * 100)
                self.update_progress_signal.emit(new_val)

    async def worker(self, link, session, headers=None):
        headers = headers or {}
        async with self.semaphore:
            return await get_video_info(link, session,
                                        progress_inc=self.progress_bar_inc, args=self._add_args,
                                        headers=headers)

    async def start_loop(self):
        try:
            async with aiohttp.ClientSession() as session:
                atasks = [self.worker(link.strip(), session) for link in self.tasks]
                self.results = await asyncio.gather(*atasks)
        except Exception as e:
            print(f"Error in loop...\n{e}")

    def run(self):
        try:
            self.update_progress_info('Get info about videos...')
            asyncio.run(self.start_loop())
        except Exception as e:
            print(f"Error in starting loop...\n{e}")
        self.update_progress_info()


class DownloadThread(QThread):
    update_progress_signal = pyqtSignal(int)
    update_progress_label_signal = pyqtSignal(str)
    add_progress_label_signal = pyqtSignal((bool, str))
    error_signal = pyqtSignal(str)

    def __init__(self, table, saving_path: str, parent=None,
                 download_info_key=True, download_video_key=True, **kwargs):
        super().__init__(parent)
        self._table = table
        self.download_info_key = download_info_key
        self.download_video_key = download_video_key
        self._saving_path = saving_path
        self.completed_tasks_info = [False for _ in range(len(self._table.model().get_data()))]

    def update_progress_info(self, label_text: str = None, bar_value: int = 0):
        self.update_progress_label_signal.emit(label_text)
        self.update_progress_signal.emit(bar_value)

    def update_progress_bar(self, value: int = 0):
        self.update_progress_signal.emit(value)

    def add_progress_label(self, add_key: bool = False, text: str = ''):
        self.add_progress_label_signal(add_key, text)

    def show_error(self, text: str):
        self.error_signal.emit(text)


    def run_download_process(self):
        if self.download_info_key:
            self.update_progress_info('Creating files...')
            save_videos_info(table=self._table,
                             saving_path=self._saving_path,
                             completed_tasks_info=self.completed_tasks_info,
                             thread=self)
        if self.download_video_key:
            self.completed_tasks_info = [False for _ in
                                         range(len(self._table.model().get_data()))]
            self.update_progress_info('Downloading videos...')
            start_video_download(table=self._table, saving_path=self._saving_path,
                                 completed_tasks_info=self.completed_tasks_info,
                                 params=OutsideYT.download_video_params,
                                 add_to_folder=self.download_info_key,
                                 thread=self)

    def run(self):
        self.run_download_process()
        self.update_progress_info()


def start_video_download(table: QTableView, saving_path: str, completed_tasks_info: List,
                         params: dict, add_to_folder: bool,
                         thread):
    data = table.model().get_data()
    videos = data[data['Selected'] > 0]
    cnt_videos = len(videos)
    for num, video in videos.iterrows():
        try:
            thread.update_progress_info(f"{num + 1}/{cnt_videos} - {video['Video']}")
            if add_to_folder:
                saving_path = os.path.join(saving_path, check_folder_name(video['Video']))
                os.makedirs(saving_path, exist_ok=True)
                video_down = OutsideDownloadVideoYT(get_video_link(video['Link'], 'embed'),
                                                    video_info=video['_download_info'],
                                                    params=params,
                                                    callback_func=thread.update_progress_bar,
                                                    callback_err=thread.show_error)
                if video_down.download_video(saving_path=saving_path):
                    completed_tasks_info[num] = True
        except Exception as e:
            print(f'Error on start downloading...\n{e}')


def save_videos_info(table, saving_path: str, completed_tasks_info: List, thread):
    data = table.model()._data
    videos_info = data.loc[data['Selected'] > 0]
    cnt_videos = len(videos_info)
    for num, video in videos_info.iterrows():
        if create_video_folder(video_info=video['_download_info'], saving_path=saving_path):
            thread.update_progress_bar(int((num + 1) / cnt_videos * 100))
            completed_tasks_info[num] = True
