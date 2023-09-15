import asyncio
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import QTableView, QPushButton, QProgressBar, QWidget


class WorkerThread(QThread):

    def __init__(self, progress_bar, process, total_steps: int):
        super().__init__()
        self.progress_bar = progress_bar
        self.process = process
        self.total_steps = total_steps

    def run(self):
        print("start progress bar...")
        for i in self.process():
            if self.total_steps == 0:
                self.total_steps = i
                continue
            if i == "End":
                break
            time.sleep(0.1)
            progress = int((i / self.total_steps) * 100)
            self.progress_bar.setValue(progress)
        self.progress_bar.setValue(0)


class WatchProgress:
    def __init__(self, total_steps):
        self.mutex = QMutex()
        self.progress = 0
        self.total_steps = total_steps


class WatchThread(QThread):
    def __init__(self, progress_bar, process, group_progress):
        super().__init__()
        self.progress_bar = progress_bar
        self.process = process
        self.group_progress = group_progress

    def run(self):
        print("start progress bar...")
        for i in self.process():
            if i == "End":
                break
            time.sleep(0.1)

            self.group_progress.mutex.lock()
            self.group_progress.progress += 1
            self.group_progress.mutex.unlock()

            progress = int((self.group_progress.progress / self.group_progress.total_steps) * 100)
            self.progress_bar.setValue(progress)
        self.progress_bar.setValue(0)


def start_operation(dialog, dialog_settings, page: str, progress_bar: QProgressBar, process, total_steps: int = 0):
    current_tab = dialog.findChild(QWidget, page)
    tab_elements = current_tab.findChildren(QWidget)

    def finish_operation():
        for el in tab_elements:
            el.setEnabled(True)
        dialog_settings.worker_thread.deleteLater()

    for el in tab_elements:
        el.setEnabled(False)

    dialog_settings.worker_thread = WorkerThread(progress_bar, process=process, total_steps=total_steps)
    dialog_settings.worker_thread.finished.connect(finish_operation)
    dialog_settings.worker_thread.start()


def start_watch_operation(dialog, dialog_settings, page: str, progress_bar: QProgressBar, process, group_progress):
    current_tab = dialog.findChild(QWidget, page)
    tab_elements = current_tab.findChildren(QWidget)

    def finish_operation():
        for el in tab_elements:
            el.setEnabled(True)
        dialog_settings.worker_thread.deleteLater()

    for el in tab_elements:
        el.setEnabled(False)

    dialog_settings.worker_thread = WatchThread(progress_bar, process=process, group_progress=group_progress)
    dialog_settings.worker_thread.finished.connect(finish_operation)
    dialog_settings.worker_thread.start()
