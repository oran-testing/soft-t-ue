import threading

from common.utils import kill_subprocess, start_subprocess


class GnuRadio:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.output = ""
        self.initialized = False
        self.name = "GNU Radio"

    def start(self, filename):
        self.process = start_subprocess(["python3", filename])
        self.isRunning = True

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False

    def __repr__(self):
        return f"{self.name}, running: {self.isRunning}"
