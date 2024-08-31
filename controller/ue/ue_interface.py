import threading
import time
import os
import sys
import select
import socket


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from common.utils import start_subprocess, kill_subprocess
from common.iperf_interface import Iperf
from common.ping_interface import Ping


class Ue:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.iperf_client = Iperf()
        self.ping_client = Ping()
        self.output = ""

    def send_command(self, ip, port, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                sock.sendall(command.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred: {e}")



    def start(self, args, ue_id):
        command = ["sudo", "srsue"] + args
        self.process = start_subprocess(command)
        os.system("sudo ip netns add ue1")
        time.sleep(1)
        os.system("sudo ip ro add 10.45.0.0/16 via 10.53.1.2")
        os.system("sudo ip netns exec ue1 ip ro add default via 10.45.1.1 dev tun_srsue")
        self.send_command("127.0.0.1", 5000, str(5000 + ue_id))
        self.iperf_client.start(['-c', '10.53.1.1','-i', '1', '-t', '3000', '-u', '-b', '100M', '-p', str(5000 + ue_id), '-R'], process_type='client')
        self.ping_client.start(['10.53.1.1'])
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
                    self.output += line
            else:
                self.output += "Process Terminated"
                self.isRunning = False
                break

    def __repr__(self):
        return f"srsRAN UE object, running: {self.isRunning}"

if __name__ == "__main__":
    handle = Ue()
    handle.start(["/home/ntia/soft-t-ue/configs/zmq/ue_zmq.conf"], 1)
    time.sleep(20)
    while True:
        sys.stdout.write(handle.output)
        sys.stdout.flush()
        sys.stdout.write(handle.iperf_client.output)
        sys.stdout.flush()
        time.sleep(0.5)

