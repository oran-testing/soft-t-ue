from utils import start_subprocess, kill_subprocess
from iperf_interface import Iperf
import threading
import time

class Ue:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.iperf_client = Iperf()
        self.output = ""

    def start(self, args):
        command = ["sudo", "srsue"] + args
        self.process = start_subprocess(command)
        self.iperf_client.start(['-c', '10.53.1.1', '-t', '3000', '-u', '-b', '10M'], process_type='client')
        self.isRunning = True

        self.log_thread = threading.Thread(target=self.collect_logs, daemon=True)
        self.log_thread.start()

    def stop(self):
        kill_subprocess(self.process)
        self.iperf_client.stop()
        self.isRunning = False

    def collect_logs(self):
        while self.isRunning:
            if self.process:
                line = self.process.stdout.readline()
                if line:
                    self.output += '\n' + line.decode().strip()
            else:
                self.output += "Process Terminated"
                break

    def __repr__(self):
        return f"srsRAN UE object, running: {self.isRunning}"

if __name__ == "__main__":
    handle = Ue()
    handle.start(["/home/ntia/Downloads/ue_zmq.conf", "--rrc.sdu_fuzzed_bits", "1", "--rrc.sdu_target_message", "RRCSetupRequest"])
    while True:
        print(handle.output)
        time.sleep(0.5)

