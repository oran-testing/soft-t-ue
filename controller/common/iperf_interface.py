from common.utils import start_subprocess, kill_subprocess
import threading
import time
import select
import sys

class Iperf:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.output = ""
        self.initialized = False
        self.name = "Iperf -- Stopped"

    def start(self, args, process_type="server"):
        if process_type == "server":
            command = ["iperf3", "-s"] + args
        elif process_type == "client":
            command = ["sudo", "ip", "netns","exec", "ue1", "iperf3"] + args
        else:
            raise ValueError("Invalid Process Type")
            return
        self.process = start_subprocess(command)
        self.isRunning = True
        self.name = f"Iperf -- {process_type}"

        self.log_thread = threading.Thread(target=self.collect_logs, daemon=True)
        self.log_thread.start()
        time.sleep(5)
        self.initialized = True

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False
        self.name = "Iperf -- Stopped"

    def collect_logs(self):
        stdout_fd = self.process.stdout.fileno()
        stderr_fd = self.process.stderr.fileno()
        poll = select.poll()
        poll.register(stdout_fd, select.POLLIN)
        poll.register(stderr_fd, select.POLLIN)

        while self.isRunning:
            events = poll.poll()
            for fd, event in events:
                if fd == stdout_fd:
                    line = self.process.stdout.readline().decode()
                    if line:
                        self.output += f"{line.strip()}\n"
                    else:
                        poll.unregister(stdout_fd)
                if fd == stderr_fd:
                    line = self.process.stderr.readline().decode()
                    if line:
                        self.output += f"[Error]: {line.strip()}\n"
                    else:
                        poll.unregister(stderr_fd)

    def __repr__(self):
        return f"Iperf Process Object, running: {self.isRunning}"

