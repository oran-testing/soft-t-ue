import threading
import time

from common.utils import kill_subprocess, start_subprocess


class Gnb:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.output = ""
        self.name = "srsRAN gNB"

    def start(self, args):
        command = ["gnb", "-c"] + args
        self.process = start_subprocess(command)
        self.isRunning = True

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False

    def __repr__(self):
        return f"{self.name}, running: {self.isRunning}"
