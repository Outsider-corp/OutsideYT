import asyncio
import time

from PyQt5.QtCore import QMutex, QThread
from PyQt5.QtWidgets import QProgressBar, QWidget


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


class WatchProgress:
    def __init__(self, total_steps: int) -> None:
        self.mutex = QMutex()
        self.progress = 0
        self.total_steps = total_steps


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

class AsyncWatchThread(QThread):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loop = asyncio.new_event_loop()
        self.videos = []

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.main())
        self.loop.close()
        self.finished.emit()

    def add_video(self, start_video):
        self.videos.append(start_video)

    async def main(self):
        await asyncio.gather(*self.videos)


class WatchThread(QThread):
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
