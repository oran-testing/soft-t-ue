import re
import select
import sys
import threading
import os
import time
from datetime import datetime

from utils import kill_subprocess, start_subprocess


class Iperf:
    def __init__(self, send_message_callback):
        self.isRunning = False
        self.process = None
        self.output = []
        self.initialized = False
        self.name = "Iperf -- Stopped"
        self.process_type = ""
        self.send_callback = send_message_callback

    def start(self, args, process_type="server", ue_index=1):
        command = []
        if process_type == "server":
            command = ["stdbuf","-oL","-eL","iperf3"] + args
        elif process_type == "client":
            command = ["ip", "netns","exec", f"ue{ue_index}", "stdbuf", "-oL", "-eL", "iperf3"] + args
        else:
            raise ValueError("Invalid Process Type")
            return
        os.system("ip ro add 10.45.0.0/16 via 10.53.1.2 > /dev/null 2>&1")
        os.system(f"ip netns exec ue{ue_index} ip ro add default via 10.45.1.1 dev tun_srsue > /dev/null 2>&1")
        time.sleep(2)
        self.process = start_subprocess(command)
        self.isRunning = True
        self.name = f"Iperf -- {process_type}"
        self.start_time = datetime.now()

        self.log_thread = threading.Thread(target=self.collect_logs, daemon=True)
        self.log_thread.start()
        self.initialized = True
        self.process_type = process_type

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False
        self.name = "Iperf -- Stopped"

    def collect_logs(self):
        bitrate_pattern = re.compile(r'(\d+\.\d+) Mbits/sec')
        while self.isRunning:
            if self.process:
                line = self.process.stdout.readline()
                if line:
                    if self.process_type == "server":
                        self.output.append(line)
                    else:
                        bitrate = bitrate_pattern.findall(line)
                        if len(bitrate) > 0:
                            self.output.append(
                                ((datetime.now() - self.start_time).total_seconds(),
                                float(bitrate[0]))
                            )
                            self.send_callback("brate", bitrate[0])

            else:
                self.output.append(0.0)
                self.isRunning = False
                break

    def __repr__(self):
        return f"Iperf Process Object, running: {self.isRunning}"

