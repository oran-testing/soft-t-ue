import re
import select
import sys
import threading
import os
import time
import csv
from datetime import datetime

from utils import kill_subprocess, start_subprocess


class Metrics:
    def __init__(self, send_message_callback):
        self.output = []
        self.isRunning = False
        self.send_callback = send_message_callback

    def get_metrics_config(self, file_path):
        keys = ["metrics_csv_enable", "metrics_csv_filename"]
        metrics_config = {}

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            for line in lines:
                # Strip whitespace and skip empty or comment lines
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or stripped.startswith(";"):
                    continue

                # Check if line contains any of the keys
                for key in keys:
                    if stripped.startswith(key):
                        # Split the line by '=' and trim spaces
                        _, value = stripped.split("=", 1)
                        metrics_config[key] = value.strip()
                        break

            # Ensure all required keys are found
            for key in keys:
                if key not in metrics_config:
                    raise KeyError(f"Key '{key}' not found in the file.")

            metrics_config["metrics_csv_enable"] = metrics_config["metrics_csv_enable"].lower() == "true"

            return metrics_config

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' was not found.")
        except ValueError as e:
            raise ValueError(f"Error processing file '{file_path}': {e}")
    
        return metrics_config

    def start(self, config_path):
        metrics_config = self.get_metrics_config(config_path)
        if not metrics_config["metrics_csv_enable"]:
            return
        self.file_path = metrics_config["metrics_csv_filename"]
        self.isRunning = True
        self.log_thread = threading.Thread(target=self.report_new_metric, daemon=True)
        self.log_thread.start()

    def report_new_metric(self):
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            lines = list(reader)  # Load all lines initially

        last_index = -1  # Keep track of the last read line
        while True:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file, delimiter=';')
                lines = list(reader)
                if len(lines) > last_index:  # If new data exists
                    for i in range(last_index, len(lines) - 1):
                        for key, value in lines[i].items():
                            if value:
                                self.send_callback(key, value)
                    last_index = len(lines)
            time.sleep(1)  # Wait for 1 second

    def __repr__(self):
        return f"Metrics Manager Process Object, running: {self.isRunning}"

if __name__ == "__main__":
    # test class functionality
    test = Metrics(lambda msg_type, msg_text: print(msg_type + " : " + msg_text))
    test.start("../../../configs/zmq/ue_zmq.conf")
    while True:
        time.sleep(1)
