from utils import start_subprocess, kill_subprocess

class UeInterface:
    def __init__(self):
        self.isRunning = False
        self.process = None

    def start(self, args):
        command = ["sudo", "srsue"] + args
        self.process = start_subprocess(command)
        self.isRunning = True

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False

    def __repr__(self):
        return f"srsRAN UE object, running: {self.isRunning}"

