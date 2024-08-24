import threading
import time

from common.utils import start_subprocess, kill_subprocess
from common.iperf_interface import Iperf


class Gnb:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.output = ""
        self.initialized = False
        self.name = "srsRAN gNB"
        self.iperf_server = Iperf()

    def start(self, args):
        command = ["sudo", "gnb", "-c"] + args
        self.process = start_subprocess(command)
        self.iperf_server.start(['-s', '-i', '1'])
        self.isRunning = True

        self.log_thread = threading.Thread(target=self.collect_logs,
                                           daemon=True)
        self.log_thread.start()
        time.sleep(5)
        self.initialized = True

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False

    def collect_logs(self):
        while self.isRunning:
            if self.process:
                line = self.process.stdout.readline()
                if line:
                    self.output += line
            else:
                self.output += "Process Terminated"
                self.isRunning = False
                break

    def __repr__(self):
        return f"{self.name}, running: {self.isRunning}"
