import asyncio
import time
import os
import threading
from Iperf import Iperf
from Ping import Ping
from utils import kill_subprocess, send_command, start_subprocess
import websockets

class Ue:
    def __init__(self, ue_index):
        self.ue_index = ue_index
        self.isRunning = False
        self.isConnected = False
        self.process = None
        self.iperf_client = Iperf()
        self.ping_client = Ping()
        self.output = ""
        self.rnti = ""
        self.websocket_clients = set()  # Track connected WebSocket clients
        self.log_queue = asyncio.Queue()  # Queue to hold logs for WebSocket

    async def websocket_handler(self, websocket, path):
        """Handle incoming WebSocket connections and stream logs to each client."""
        self.websocket_clients.add(websocket)
        try:
            while True:
                message = await self.log_queue.get()  # Wait for a log message from the queue
                await websocket.send(message)  # Send the message to the client
                self.log_queue.task_done()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.websocket_clients.remove(websocket)  # Remove client on disconnect

    def start_websocket_server(self):
        """Start the WebSocket server in a separate thread."""
        self.websocket_thread = threading.Thread(target=self.run_websocket_server, daemon=True)
        self.websocket_thread.start()

    def run_websocket_server(self):
        """Run the WebSocket server for sending logs."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.websocket_handler, "localhost", 8765 + self.ue_index)
        loop.run_until_complete(start_server)
        loop.run_forever()

    def start(self, args, mode="baremetal"):
        if mode == "docker":
            # Docker setup if needed
            pass
        else:
            command = ["sudo", "srsue"] + args
            self.process = start_subprocess(command)
            self.isRunning = True
            self.stop_thread = threading.Event()

            # Start the WebSocket server
            self.start_websocket_server()

            # Start the log collection thread
            self.log_thread = threading.Thread(target=self.collect_logs, daemon=True)
            self.log_thread.start()

    def start_metrics(self):
        # Define start_metrics logic
        pass

    def stop(self):
        self.stop_thread.set()
        kill_subprocess(self.process)
        self.iperf_client.stop()
        self.isRunning = False

    def collect_logs(self):
        """Collect logs from the process and add them to the log queue for the WebSocket server."""
        while self.isRunning and not self.stop_thread.is_set():
            if self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    self.output += line
                    if "rnti" in line:
                        self.rnti = line.split("0x")[1][:4]
                    if "PDU" in line:
                        self.start_metrics()
                        self.isConnected = True
                    
                    # Add the log line to the queue for broadcasting
                    asyncio.run(self.log_queue.put(line))
            else:
                # If the process terminates, send a termination message
                asyncio.run(self.log_queue.put("Process Terminated"))
                self.isRunning = False
                break

    def __repr__(self):
        return f"srsRAN UE{self.ue_index} object, running: {self.isRunning}"


if __name__ == "__main__":
    test = Ue(1)
    test.start(["./configs/zmq/ue_zmq.conf"])
    while True:
        time.sleep(1)
        print(test.output)

