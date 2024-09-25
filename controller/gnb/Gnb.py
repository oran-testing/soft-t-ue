import threading
import time
import os
import sys

# add the common directory to the import path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from common.utils import kill_subprocess, start_subprocess


class Gnb:
    def __init__(self):
        self.isRunning = False
        self.initialized = False
        self.process = None
        self.output = ""
        self.name = "srsRAN gNB"

    def start(self, args):
        command = ["gnb", "-c"] + args
        self.process = start_subprocess(command)
        self.isRunning = True
        self.log_thread = threading.Thread(target=self.collect_logs,
                                           daemon=True)
        self.log_thread.start()

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False

    def collect_logs(self):
        completed_text = "gNodeB started"
        while self.isRunning and self.process:
            line = self.process.stdout.readline()
            if line:
                self.output += line
                if completed_text in self.output:
                    self.initialized = True
            time.sleep(0.1)

        self.output += "Process Terminated"

    def __repr__(self):
        return f"{self.name}, running: {self.isRunning}"

if __name__ == "__main__":
    test = Gnb()
    test.start(["/home/ntia/soft-t-ue/configs/zmq/gnb_zmq.yaml"])
    while True:
        time.sleep(1)
        print(test)
        print(test.output)
