import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from scapy.all import *
import time

from ue_interface import UeInterface
from gnb_interface import GnbInterface

class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Sniffer")
        self.root.geometry("800x600")


        self.captured_packets = []
        self.ue = UeInterface()
        self.gnb = GnbInterface()

        # Text area to display captured packets
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=30)
        self.text_area.pack(pady=10)

        # Start button to begin packet capture
        self.start_button = tk.Button(self.root, text="Start Capture", command=self.start_capture)
        self.start_button.pack()

        # Save button to save captured packets to a file
        self.save_button = tk.Button(self.root, text="Save Capture", command=self.save_capture)
        self.save_button.pack()

    def start_capture(self):
        self.gnb.start(["-c","~/Downloads/gnb_zmq.yaml"])
        time.sleep(1)
        self.ue.start(["~/Downloads/ue_zmq.conf"])
        self.text_area.delete('1.0', tk.END)  # Clear previous text
        self.captured_packets = []  # Clear previous packets
        try:
            sniff(iface='br-e55ff388d513', prn=self.packet_handler, count=100)
        except PermissionError:
            messagebox.showerror("Permission Error", "Permission denied. Try running as root or administrator.")

    def packet_handler(self, packet):
        self.captured_packets.append(packet)
        self.text_area.insert(tk.END, packet.summary() + "\n")
        self.text_area.see(tk.END)  # Scroll to the end of the text area

    def save_capture(self):
        if self.captured_packets:
            file_path = "captured_packets.pcap"
            wrpcap(file_path, self.captured_packets)
            messagebox.showinfo("Save Capture", f"Packets saved to {file_path}")
        else:
            messagebox.showwarning("Save Capture", "No packets to save")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()
