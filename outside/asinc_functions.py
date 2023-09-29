import asyncio
import time

from typing import List
import aiohttp
from PyQt5.QtCore import QMutex, QThread, QMetaObject, Qt, QGenericArgument, pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QProgressBar, QWidget, QTableView

import OutsideYT
from outside.Download.functions import _get_download_saving_path, create_video_folder
from outside.YT_functions import get_video_info, watching
from outside.functions import get_video_link
from outside.message_boxes import error_func


class WorkerThread(QThread):

    def __init__(self, progress_bar, process, total_steps: int) -> None:
        super().__init__()
        self.progress_bar = progress_bar
        self.process = process
        self.total_steps = total_steps

    def run(self):
        print('start progress bar...')
        for i in self.process():
            if self.total_steps == 0:
                self.total_steps = i
                continue
            if i == 'End':
                break
            time.sleep(0.1)
            progress = int((i / self.total_steps) * 100)
            self.progress_bar.setValue(progress)
        self.progress_bar.setValue(0)


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


class WatchThreadOneProgressBar(QThread):
    def __init__(self, progress_bar, process, group_progress) -> None:
        super().__init__()
        self.progress_bar = progress_bar
        self.process = process
        self.group_progress = group_progress

    def run(self):
        print('start progress bar...')
        for i in self.process():
            if i == 'End':
                break
            time.sleep(0.1)

            self.group_progress.mutex.lock()
            self.group_progress.progress += 1
            self.group_progress.mutex.unlock()

            progress = int((self.group_progress.progress / self.group_progress.total_steps) * 100)
            self.progress_bar.setValue(progress)


class GetVideoInfoThread(QThread):
    _loop = asyncio.new_event_loop()

    def __init__(self, tasks: list, progress_bar=None, progress_label=None,
                 parent=None, **kwargs) -> None:
        super().__init__(parent)
        self.tasks = tasks
        self.results = []
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.lock = asyncio.Lock()
        self.total_steps = len(tasks)
        self.progress = 0
        self._add_args = kwargs

    async def progress_bar_inc(self):
        await asyncio.sleep(0.01)
        if self.progress_bar:
            async with self.lock:
                self.progress += 1
                new_val = int(self.progress / self.total_steps * 100)
                self.progress_bar.setValue(new_val)

    async def start_loop(self):
        async with aiohttp.ClientSession() as session:
            atasks = [get_video_info(link.strip(), session,
                                     progress_inc=self.progress_bar_inc, **self._add_args) for link
                      in self.tasks]
            self.results = await asyncio.gather(*atasks)

    def run_loop(self):
        if self.progress_label:
            self.progress_label.setText('Get info about videos...')
        if self.progress_bar:
            self.progress_bar.setValue(0)
        asyncio.set_event_loop(GetVideoInfoThread._loop)
        GetVideoInfoThread._loop.run_until_complete(self.start_loop())
        if self.progress_bar:
            self.progress_bar.setValue(0)

    def run(self):
        self.run_loop()
        if self.progress_label:
            self.progress_label.clear()
        if self.progress_bar:
            self.progress_bar.setValue(0)


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


class DownloadThread(GetVideoInfoThread):
    def __init__(self, table, dialog, dialog_settings, saving_path: str,
                 tasks: list, progress_bar=None, progress_label=None, parent=None,
                 download_info=True, download_video=True, **kwargs):
        super().__init__(tasks=tasks, progress_bar=progress_bar,
                         progress_label=progress_label, parent=parent, **kwargs)
        self._table = table
        self._dialog = dialog
        self._dialog_settings = dialog_settings
        self.download_info = download_info
        self.download_video = download_video
        self._saving_path = saving_path

    def run(self):

        if self.download_info:
            self.run_loop()
            if self.progress_label:
                self.progress_label.setText('Creating files...')
            if self.progress_bar:
                self.progress_bar.setValue(0)
            save_videos_info(table=self._table, videos_info=self.results,
                             saving_path=self._saving_path)

        if self.download_video:
            start_video_download(self._dialog, self._dialog_settings, self._table)
        if self.progress_bar:
            self.progress_bar.setValue(0)
        if self.progress_label:
            self.progress_label.clear()


def start_operation(dialog, dialog_settings, page: str, progress_bar: QProgressBar, process,
                    total_steps: int = 0):
    current_tab = dialog.findChild(QWidget, page)
    tab_elements = current_tab.findChildren(QWidget)

    def finish_operation():
        for el in tab_elements:
            el.setEnabled(True)
        dialog_settings.worker_thread.deleteLater()

    for el in tab_elements:
        el.setEnabled(False)

    dialog_settings.worker_thread = WorkerThread(progress_bar, process=process,
                                                 total_steps=total_steps)
    dialog_settings.worker_thread.finished.connect(finish_operation)
    dialog_settings.worker_thread.start()


def start_video_download(dialog, dialog_settings, table: QTableView):
    pass


def save_videos_info(table, videos_info: List, saving_path: str):
    for video in videos_info:
        create_video_folder(table, video_info=video, saving_path=saving_path)
