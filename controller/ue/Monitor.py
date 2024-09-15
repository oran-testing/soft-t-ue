import os
import select
import socket
import sys
import threading
import time
import re
import psutil


class Monitor:
    def __init__(self):
        self.monitor_list = {}
        self.thread_list = {}

    def monitor_process(self, name, regex_string):
        stop_event = threading.Event()
        log_thread = threading.Thread(target=self.check_processes, args=(re.compile(regex_string), stop_event, name), daemon=True)
        log_thread.start()
        self.thread_list[name] = {"thread": log_thread, "event": stop_event}
        self.monitor_list[name] = False

    def stop(self):
        for key, thread_map in self.thread_list.items():
            thread_map["event"].set()


    def check_processes(self, regex_pattern, stop_event, process_name):
        while not stop_event.is_set():
            self.monitor_list[process_name] = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if regex_pattern.search(cmdline):
                        self.monitor_list[process_name] = True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            time.sleep(5)

    def __repr__(self):
        return f"Process Monitor object, result: {self.monitor_list}"

if __name__ == "__main__":
    print("TESTING: Monitor")
    monitor = Monitor()
    monitor.monitor_process("gnb", r'gnb -c')
    while True:
        time.sleep(1)
        print(monitor)
