import asyncio
import time

from typing import List
import aiohttp
from PyQt5.QtCore import QMutex, QThread, QMetaObject, Qt, QGenericArgument, pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QProgressBar, QWidget

import OutsideYT
from outside.YT_functions import get_video_info, watching


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
    def __init__(self, threads_list, elements_list, dialog_settings) -> None:
        super().__init__()
        self.threads_list = threads_list
        self.elements_list = elements_list
        self.dialog_settings = dialog_settings

    def run(self):
        while True:
            if not self.threads_list:
                self.dialog_settings.Watch_Table.hideColumn(
                    list(self.dialog_settings.Watch_Table.model().get_data().columns).index(
                        'Progress'))
                self.dialog_settings.Watch_Table.setColumnHidden(
                    list(self.dialog_settings.Watch_Table.model().get_data().columns).index('id'),
                    False)
                for el in self.elements_list:
                    el.setEnabled(True)
                break


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


class WatchThreadOld(QThread):
    def __init__(self, progress_bar, process, group_progress) -> None:
        super().__init__()
        self.progress_bar = progress_bar
        self.process = process
        self.group_progress = group_progress

    def run(self):
        for i in self.process():
            if i == 'End':
                break
            time.sleep(0.1)

            self.group_progress.mutex.lock()
            self.group_progress.progress += 1
            self.group_progress.mutex.unlock()

            progress = int((self.group_progress.progress / self.group_progress.total_steps) * 100)
            self.progress_bar(value=progress)


class GetVideoInfoThread(QThread):

    def __init__(self, tasks: list, table, parent=None) -> None:
        super().__init__(parent)
        self.table = table
        self.tasks = tasks
        self.results = []
        self.progress_bar = table.model().progress_bar
        self.lock = asyncio.Lock()
        self.total_steps = len(tasks)
        self.progress = 0

    async def progress_bar_inc(self):
        await asyncio.sleep(0.005)
        async with self.lock:
            self.progress += 1
            new_val = int(self.progress / self.total_steps * 100)
            self.progress_bar.setValue(new_val)

    async def start_loop(self):
        async with aiohttp.ClientSession() as session:
            atasks = [get_video_info(link.strip(), session, progress_inc=self.progress_bar_inc)
                      for link in self.tasks]
            self.results = await asyncio.gather(*atasks)

    def run(self):
        asyncio.run(self.start_loop())
        self.progress_bar.setValue(0)


class WatchThread(QThread):

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
            qindex = self._table.model().index(self._progress_bar_num, 1, QModelIndex())

    async def start_loop(self):
        atasks = [watching(self._video, self._durations, user,
                           driver_headless=self.driver_headless,
                           progress_inc=self.progress_bar_inc)
                  for user in self._users]
        await asyncio.gather(*atasks)

    def run(self):
        asyncio.run(self.start_loop())


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


def start_watch_operation(dialog_settings, progress_bar, process, group_progress):
    def finish_operation():
        try:
            worker_thread.deleteLater()
            dialog_settings.watch_threads.remove(worker_thread)
        except:
            pass

    worker_thread = WatchThread(progress_bar, process=process, group_progress=group_progress)
    dialog_settings.watch_threads.append(worker_thread)
    worker_thread.finished.connect(finish_operation)
    worker_thread.start()
