import asyncio

from typing import List, Dict
import aiohttp
from PyQt5.QtCore import QMutex, QThread, pyqtSignal, QObject, QThreadPool, QRunnable

import OutsideYT
from outside.Download.functions import start_video_download, save_videos_info
from outside.YT.functions import get_video_info, watching_selenium, watching_playwright
from outside.functions import get_video_link


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


class WatchSignals(QObject):
    progress_signal = pyqtSignal((int, int))
    finished_signal = pyqtSignal()


class Watcher(QRunnable):

    def __init__(self, _id, video_info: Dict, watchers: List, driver_headless=True,
                 offsets: List = None):
        super().__init__()
        self.__id = _id
        self._video_info = video_info
        self._watchers = watchers
        self.driver_headless = driver_headless
        self._offsets = offsets
        self.signals = WatchSignals()

        sum_offsets = sum(offsets) if offsets else 0
        self._total_steps = len(self._watchers) * int(self._video_info['Duration']) + sum_offsets
        self._lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(OutsideYT.ASYNC_LIMIT)
        self._progress = 0

    async def progress_bar_inc(self, val: int = 1):
        async with self._lock:
            self._progress += val
            new_val = int(self._progress / self._total_steps * 100)
            self.signals.progress_signal.emit(self.__id, new_val)

    async def watching(self, user):
        async with self.semaphore:
            await watching_playwright(get_video_link(self._video_info['Link'], type='watch'),
                                      int(self._video_info['Duration']), user,
                                      driver_headless=self.driver_headless,
                                      progress_inc=self.progress_bar_inc)

    async def start_loop(self):
        atasks = [self.watching(user) for user in self._watchers]
        await asyncio.gather(*atasks)
        self.signals.progress_signal.emit(self.__id, 100)

    def run(self):
        asyncio.run(self.start_loop())
        self.signals.finished_signal.emit()


class WatchManager(QObject):
    update_progress_watcher_signal = pyqtSignal((int, int))
    finish_signal = pyqtSignal()

    def __init__(self, max_workers: int):
        super().__init__()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(max_workers)
        self._watchers = {}

    def add_watcher(self, _id, video_info: Dict, watchers: List, offsets: List = None,
                    driver_headless=True, auto_start=False, **kwargs):
        watcher = Watcher(_id, video_info, watchers, driver_headless, offsets)
        self._watchers[_id] = watcher
        watcher.signals.progress_signal.connect(
            lambda _id1, x: self.handle_watcher_progress(_id1, x))
        watcher.signals.finished_signal.connect(self.finish)
        if auto_start:
            self.start_watcher(_id)

    def start_watcher(self, _id):
        self.threadpool.start(self._watchers[_id])

    def handle_watcher_progress(self, _id: int, value: int):
        self.update_progress_watcher_signal.emit(_id, value)

    def finish(self):
        if self.threadpool.activeThreadCount() == 0:
            self.finish_signal.emit()


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

    def __init__(self, videos: List, saving_path: str, parent=None,
                 download_info_key=True, download_video_key=True, **kwargs):
        super().__init__(parent)
        self.download_info_key = download_info_key
        self.download_video_key = download_video_key
        self._saving_path = saving_path
        self.videos = videos
        self.completed_tasks_info = [False for _ in range(len(videos))]

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
            save_videos_info(videos=self.videos,
                             saving_path=self._saving_path,
                             completed_tasks_info=self.completed_tasks_info,
                             thread=self)
        if self.download_video_key:
            self.completed_tasks_info = [False for _ in range(len(self.videos))]
            self.update_progress_info('Downloading videos...')
            start_video_download(videos=self.videos, saving_path=self._saving_path,
                                 completed_tasks_info=self.completed_tasks_info,
                                 params=OutsideYT.download_video_params,
                                 add_to_folder=self.download_info_key,
                                 thread=self)

    def run(self):
        self.run_download_process()
        self.update_progress_info()
