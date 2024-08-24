import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


from common.utils import start_subprocess, kill_subprocess
import threading
import re

class Ping:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.output = []
        self.initialized = False
        self.name = "Ping -- Stopped"
        self.process_type = ""

    def start(self, args):
        # Construct the ping command
        command = ["ping"] + args
        self.process = start_subprocess(command)
        self.isRunning = True
        self.name = "Ping -- Running"

        self.log_thread = threading.Thread(target=self.collect_logs, daemon=True)
        self.log_thread.start()
        self.initialized = True

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False
        self.name = "Ping -- Stopped"

    def collect_logs(self):
        latency_pattern = re.compile(r'time=(\d+\.?\d*) ms')
        while self.isRunning:
            if self.process:
                line = self.process.stdout.readline()
                if line:
                    latency = latency_pattern.findall(line)
                    if latency:
                        self.output.append(float(latency[0]))

            else:
                self.output.append(0.0)
                self.isRunning = False
                break

    def __repr__(self):
        return f"Ping Process Object, running: {self.isRunning}"

if __name__ == "__main__":
    ping_handle = Ping()
    ping_handle.start(["8.8.8.8"])
    while True:
        print(ping_handle.output)
