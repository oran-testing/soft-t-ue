import itertools
import sys
import threading
import time

import tailer

from core_interface import CoreNetwork
from gnb_interface import Gnb
# from iperf_interface import Iperf


class gnb_controller:
    def start(self):
        # connect to ue controller

        # recieve configuration

        # start gnb and core
        self.core_handle = CoreNetwork()
        self.core_handle.start()
        self.spinner_loading(self.core_handle)

        print("\n\nCore Started Successfully!")
        print("Starting gNB...")

        self.gnb_handle = Gnb()
        self.gnb_handle.start([sys.argv[1]])

        # sending metrics
        self.gnb_logs_process = threading.Thread(
            target=self.get_gnb_logs).start()
        # stop gnb, core, metrics, etc
        # run a variation of main without calling ue_controller

    def get_gnb_logs(self):
        for line in tailer.follow(open("/tmp/gnb.log")):
            # TODO: Fix this poor handling of the output.
            print(line)

    def spinner_loading(self, handle, verbose=True):
        spinner = itertools.cycle(["|", "/", "-", "\\"])
        while not handle.initialized:
            if verbose:
                sys.stdout.write(handle.output + "\n\n" + 50 * "=" + "\n")
            sys.stdout.write(f"{handle.name} " + next(spinner))
            sys.stdout.flush()
            sys.stdout.write("\b")
            time.sleep(0.1)


if __name__ == "__main__":
    controller = gnb_controller()
    controller.start()
    while controller.gnb_handle.isRunning and controller.core_handle.isRunning:
        time.sleep(0.5)
        print(f"\n\n{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n")
        # Core Network Logs
        print(f"✨ {controller.core_handle}")
        core_end = '\n\t'.join(controller.core_handle.output.split('\n')[-5:])
        print(f"\t{core_end}\n\n")
        # GNB Logs
        print(f"✨ {controller.gnb_handle}")
        gnb_end = '\n\t'.join(controller.gnb_handle.output.split('\n')[-5:])
        print(f"\t{gnb_end}\n\n")
        #  Iperf Server Logs
        print(f"✨ {controller.gnb_handle.iperf_server}")
        iperf_end = '\n\t'.join(controller.gnb_handle.iperf_server.output.split('\n')[-5:])
        print(f"\t{iperf_end}\n\n")
