import asyncio
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
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
            if self.total_steps is None:
                self.total_steps = i
                continue
            time.sleep(0.1)
            progress = int((i / self.total_steps) * 100)
            self.progress_bar.setValue(progress)
        self.progress_bar.setValue(0)


def start_operation(dialog, dialog_settings, page: str, progress_bar: QProgressBar, process, total_steps: int=None):
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
