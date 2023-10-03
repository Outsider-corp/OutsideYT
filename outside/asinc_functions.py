import asyncio
import os
import time

from typing import List
import aiohttp
from PyQt5.QtCore import QMutex, QThread, pyqtSignal
from PyQt5.QtWidgets import QTableView

import OutsideYT
from outside.Download.functions import create_video_folder
from outside.YT_functions import get_video_info, watching, download_video_dlp
from outside.functions import check_folder_name
from outside.message_boxes import error_func


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


class SeekThreads(QThread):
    def __init__(self, threads_list, dialog_settings) -> None:
        super().__init__()
        self.threads_list = threads_list
        self.dialog_settings = dialog_settings

    def run(self):
        while self.threads_list:
            pass


class GetVideoInfoThread(QThread):
    # finished_signal = pyqtSignal()

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
        self.semaphore = asyncio.Semaphore(OutsideYT.semaphore_limit)

    def update_progress_info(self, label_text: str, bar_value: int):
        if self.progress_label:
            self.progress_label.setText(label_text)
        if self.progress_bar:
            self.progress_bar.setValue(bar_value)

    async def progress_bar_inc(self):
        await asyncio.sleep(0.03)
        async with self.lock:
            if self.progress_bar:
                self.progress += 1
                new_val = int(self.progress / self.total_steps * 100)
                self.progress_bar.setValue(new_val)

    async def worker(self, link, session):
        async with self.semaphore:
            print(3)
            return await get_video_info(link, session,
                                        progress_inc=self.progress_bar_inc, args=self._add_args)

    async def start_loop(self):
        try:
            print(1)
            async with aiohttp.ClientSession() as session:
                print(2)
                atasks = [self.worker(link.strip(), session) for link in self.tasks]
                self.results = await asyncio.gather(*atasks)
        except Exception as e:
            print(f"Error in loop...\n{e}")

    def run_loop(self):
        try:
            _loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_loop)
            self.semaphore = asyncio.Semaphore(OutsideYT.semaphore_limit)
            self.update_progress_info('Get info about videos...', 0)
            try:
                _loop.run_until_complete(self.start_loop())
                print(9)
            finally:
                _loop.close()
            print(10)
        except Exception as e:
            print(f"Error in starting loop...\n{e}")

    def run(self):
        self.run_loop()
        print(11)
        self.update_progress_info('', 0)
        # self.finished_signal.emit()
        print(12)


class WatchThread(QThread):
    _loop = asyncio.new_event_loop()

    def __init__(self, table, table_row: int, driver_headless=True, parent=None,
                 offsets: List = None) -> None:
        super().__init__(parent)
        self._table = table
        self._video = table.model().get_data().loc[table_row, "Link"]
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

    async def progress_bar_inc(self):
        await asyncio.sleep(0.005)
        async with self._lock:
            self._progress += 1
            new_val = int(self._progress / self._total_steps * 100)
            self._table.model().update_progress_bar(self._progress_bar_num, new_val)

    async def start_loop(self):
        atasks = [watching(self._video, self._durations, user,
                           driver_headless=self.driver_headless,
                           progress_inc=self.progress_bar_inc)
                  for user in self._users]
        await asyncio.gather(*atasks)

    def run(self):
        asyncio.set_event_loop(WatchThread._loop)
        WatchThread._loop.run_until_complete(self.start_loop())
        self._table.model().reset_progress_bars()


class DownloadThread(QThread):
    def __init__(self, table, saving_path: str, progress_bar=None, progress_label=None, parent=None,
                 download_info_key=True, download_video_key=True, **kwargs):
        super().__init__(parent)
        self._table = table
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.download_info_key = download_info_key
        self.download_video_key = download_video_key
        self._saving_path = saving_path
        self.completed_tasks_info = [False for _ in range(len(self._table.model().get_data()))]

    def update_progress_info(self, label_text: str, bar_value: int):
        if self.progress_label:
            self.progress_label.setText(label_text)
        if self.progress_bar:
            self.progress_bar.setValue(bar_value)

    def run(self):
        if self.download_info_key:
            self.update_progress_info('Creating files...', 0)
            save_videos_info(table=self._table,
                             saving_path=self._saving_path,
                             completed_tasks_info=self.completed_tasks_info,
                             progress_bar=self.progress_bar)

        if self.download_video_key:
            self.completed_tasks_info = [False for _ in range(len(self._table.model().get_data()))]
            self.update_progress_info('Downloading videos...', 0)
            start_video_download(table=self._table, saving_path=self._saving_path,
                                 completed_tasks_info=self.completed_tasks_info,
                                 params=OutsideYT.download_video_params,
                                 progress_bar=self.progress_bar,
                                 progress_label=self.progress_label,
                                 add_to_folder=self.download_info_key)

        self.update_progress_info('', 0)


def start_video_download(table: QTableView, saving_path: str, completed_tasks_info: List,
                         params: dict, progress_bar, progress_label, add_to_folder: bool):
    data = table.model().get_data()
    cnt_videos = len(data)
    for num, video in data.iterrows():
        try:
            if progress_label:
                progress_label.setText(f"{num + 1}/{cnt_videos} - {video['Video']}")
            if progress_bar:
                progress_bar.setValue(0)
            if add_to_folder:
                saving_path = os.path.join(saving_path, check_folder_name(video['Video']))
                os.makedirs(os.path.join(saving_path), exist_ok=True)
            if download_video_dlp(video['Video'], video['Link'], params, saving_path, progress_bar):
                completed_tasks_info[num] = True
        except Exception as e:
            print(f'Error on start downloading...\n{e}')


def save_videos_info(table, saving_path: str, completed_tasks_info: List,
                     progress_bar):
    videos_info = table.model().get_data()
    cnt_videos = len(videos_info)
    for num, video in videos_info.iterrows():
        if video['Selected'] and create_video_folder(table, video_info=video['_download_info'],
                                                     saving_path=saving_path):
            if progress_bar:
                progress_bar.setValue((num + 1) / cnt_videos * 100)
            completed_tasks_info[num] = True
