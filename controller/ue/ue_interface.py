import threading
import time
import os
import sys
import select


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from common.utils import start_subprocess, kill_subprocess
from common.iperf_interface import Iperf
from common.ping_interface import Ping


class Ue:
    def __init__(self, ue_index):
        self.ue_index = ue_index
        self.isRunning = False
        self.process = None
        self.iperf_client = Iperf()
        self.ping_client = Ping()
        self.output = ""

    def start(self, args):
        command = ["sudo", "srsue"] + args
        self.process = start_subprocess(command)
        self.isRunning = True
        self.log_thread = threading.Thread(target=self.collect_logs, daemon=True)
        self.log_thread.start()
    
    def start_metrics(self):
        print(f"Starting UE {self.ue_index} metrics")
        os.system(f"sudo ip netns add ue{self.ue_index}")
        os.system("sudo ip ro add 10.45.0.0/16 via 10.53.1.2")
        os.system(f"sudo ip netns exec ue{self.ue_index} ip ro add default via 10.45.1.1 dev tun_srsue")
        self.iperf_client.start(['-c', '10.53.1.1','-i', '1', '-t', '3000', '-u', '-b', '100M', '-R'], process_type='client', ue_index=self.ue_index)
        self.ping_client.start(['10.53.1.1'])


    def stop(self):
        kill_subprocess(self.process)
        self.iperf_client.stop()
        self.isRunning = False

    def collect_logs(self):
        while self.isRunning:
            if self.process:
                line = self.process.stdout.readline()
                if line:
                    self.output += line
                    if "PDU" in line:
                        self.start_metrics()
            else:
                self.output += "Process Terminated"
                self.isRunning = False
                break

    def __repr__(self):
        return f"srsRAN UE{self.ue_index} object, running: {self.isRunning}"

if __name__ == "__main__":
    handle = Ue()
    handle.start(["/home/ntia/Downloads/ue_zmq.conf"])
    time.sleep(20)
    while True:
        sys.stdout.write(handle.output)
        sys.stdout.flush()
        sys.stdout.write(handle.iperf_client.output)
        sys.stdout.flush()
        time.sleep(0.5)

