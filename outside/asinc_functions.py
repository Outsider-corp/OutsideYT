import asyncio
import os
import pickle

from typing import List, Dict, Union, Any
import aiohttp
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QThreadPool, QRunnable
from playwright.async_api import async_playwright

import OutsideYT
from outside.Download.functions import start_video_download, save_videos_info
from outside.YT.functions import get_video_info, watching_playwright, \
    BrowserContextPlayWright, check_cookies_playwright, update_cookies
from outside.functions import get_video_link


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
            return await watching_playwright(get_video_link(self._video_info['Link'], type='watch'),
                                             user=user,
                                             driver_headless=self.driver_headless,
                                             progress_inc=self.progress_bar_inc)

    async def start_loop(self):
        atasks = [self.watching(user) for user in self._watchers]
        results = await asyncio.gather(*atasks)
        if all(results):
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

    def __init__(self, videos: List, download_params: Dict, saving_path: str, parent=None,
                 download_info_key=True, download_video_key=True, **kwargs):
        super().__init__(parent)
        self.download_info_key = download_info_key
        self.download_video_key = download_video_key
        self._saving_path = saving_path
        self.videos = videos
        self.download_params = download_params
        self.completed_tasks_info = [video['Selected'] for video in self.videos]

    def update_progress_info(self, bar_value: int = 0, label_text: str = None):
        self.update_progress_label_signal.emit(label_text)
        self.update_progress_signal.emit(bar_value)

    def update_progress_bar(self, value: int):
        self.update_progress_signal.emit(value)

    def add_progress_label(self, add_key: bool = False, text: str = ''):
        self.add_progress_label_signal(add_key, text)

    def show_error(self, text: str):
        self.error_signal.emit(text)

    def run_download_process(self):
        if self.download_info_key:
            self.update_progress_info(label_text='Creating files...')
            save_videos_info(videos=self.videos,
                             saving_path=self._saving_path,
                             completed_tasks_info=self.completed_tasks_info,
                             thread=self)
        if self.download_video_key:
            self.completed_tasks_info = [video['Selected'] for video in self.videos]
            self.update_progress_info(label_text='Downloading videos...')
            start_video_download(videos=self.videos, saving_path=self._saving_path,
                                 completed_tasks_info=self.completed_tasks_info,
                                 params=self.download_params,
                                 thread=self)

    def run(self):
        self.run_download_process()
        self.update_progress_info()


class CheckCookiesLifeThread(QThread):

    def __init__(self, app_settings):
        super().__init__()
        self.settings = app_settings
        self.to_delete = []

    async def check_cookies_life(self, playwright, cookies_file):
        cookies = pickle.load(open(cookies_file, 'rb'))
        async with BrowserContextPlayWright(playwright, cookies) as browser:
            page = await browser.new_page()
            await page.goto(OutsideYT.YT_URL, wait_until='domcontentloaded',
                            timeout=OutsideYT.WAIT_TIME_URL_UPLOADS * 1000)
            if await check_cookies_playwright(page):
                update_cookies(await page.context.cookies(), cookies_file)
            else:
                acc = os.path.basename(cookies_file).replace('_cookies', '')
                self.to_delete.append(acc)

    async def run_loop(self):
        async with async_playwright() as pw:
            atasks = [self.check_cookies_life(pw, os.path.join(self.settings.cookies_folder, file))
                      for file in os.listdir(self.settings.cookies_folder) if
                      file.endswith('_cookies')]
            await asyncio.gather(*atasks)

    def run(self) -> None:
        asyncio.run(self.run_loop())
