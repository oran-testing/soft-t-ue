import threading

from common.utils import kill_subprocess, start_subprocess


class MetricsServer:
    def __init__(self):
        self.isRunning = False
        self.process = None
        self.output = ""
        self.initialized = False
        self.name = "Influx & Metrics Server"

    def start(self, rebuild):
        command = list()
        if rebuild:
            command = [
                "docker",
                "compose",
                "-f",
                "/opt/srsRAN_Project/docker/docker-compose.yml",
                "up",
                "--build",
                "metrics-server",
                "influxdb"
            ]
        else:
            command = [
                "docker",
                "compose",
                "-f",
                "/opt/srsRAN_Project/docker/docker-compose.yml",
                "up",
                "metrics-server",
                "influxdb"
            ]
        self.process = start_subprocess(command)
        self.isRunning = True

        self.log_thread = threading.Thread(target=self.collect_logs,
                                           daemon=True)
        self.log_thread.start()

    def stop(self):
        kill_subprocess(self.process)
        self.isRunning = False

    def collect_logs(self):
        completed_text = "|"
        while self.isRunning:
            if self.process:
                line = self.process.stdout.readline()
                if line:
                    self.output += line
                    if completed_text in self.output:
                        self.initialized = True

            else:
                self.output += "Process Terminated"
                break

    def __repr__(self):
        return f"{self.name}, running: {self.isRunning}"
