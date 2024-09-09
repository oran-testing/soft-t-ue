import itertools
import sys
import threading
import time
import os
import pathlib
import argparse
import socket
import logging

import tailer


# add the common directory to the import path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from CoreNetwork import CoreNetwork
from Gnb import Gnb
from common.Iperf import Iperf


class gnb_controller:

    def __init__(self):
        self.core_handle = CoreNetwork()
        self.gnb_handle = Gnb()

    def start_core(self, rebuild):
        if self.core_handle.isRunning:
            self.core_handle.stop()
        self.core_handle.start(rebuild)
        while not self.core_handle.initialized:
            time.sleep(0.1)

    def stop_core(self):
        self.core_handle.stop()

    def start_gnb(self, gnb_config):
        if self.gnb_handle.isRunning:
            self.gnb_handle.stop()
        self.gnb_handle.start([gnb_config])

    def stop_gnb(self):
        self.gnb_handle.stop()


    def listen_for_command(self, server_socket, add_callback):
        while True:
            client_socket, _ = server_socket.accept()
            command = client_socket.recv(1024).decode('utf-8').strip()
            client_socket.close()

            directives = command.split(":")

            iperf_process = Iperf()
            if directives[0] == "iperf":
                iperf_process.start(["-s", "-i", "1", "-p", directives[1]], process_type="server")
                add_callback(iperf_process)
            elif directives[0] == "gnb":
                if directives[1] == "start":
                    self.start_gnb(directives[2])
                else:
                    self.stop_gnb()
            elif directives[0] == "core":
                if directives[1] == "start":
                    self.start_core(True)
                else:
                    self.stop_core()


def parse():
    current_script_path = pathlib.Path(__file__).resolve()
    repo_root = current_script_path.parent.parent.parent
    code_root = repo_root.parent
    parser = argparse.ArgumentParser(
        description="Run an srsRAN gNB and Open5GS, then send metrics to the ue_controller")
    parser.add_argument('--ip', type=str, help='IP address to listen for commands', default="127.0.0.1")
    parser.add_argument('--port', type=int, help='Port to listen for commands', default="5000")
    parser.add_argument('--rebuild_core', type=bool, help='Should the core be built before running?', default=True)
    return parser.parse_args()


def main():
    args = parse()
    print(args)
    os.system("kill -9 $(ps aux | awk '!/main\.py/ && /gnb/{print $2}')")
    os.system("kill -9 $(ps aux | awk '/open5gs/{print $2}')")
    time.sleep(0.1)
    controller = gnb_controller()
    controller.start_core(args.rebuild_core)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((args.ip, args.port))
    server_socket.listen(1)

    iperf_servers = []

    while True:
        time.sleep(1)
        controller.listen_for_command(server_socket, lambda x: iperf_servers.append(x))
    return 0

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
