import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from scapy.all import *


class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Sniffer")
        self.root.geometry("800x600")

        # Text area to display captured packets
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=30)
        self.text_area.pack(pady=10)

        # Start button to begin packet capture
        self.start_button = tk.Button(self.root, text="Start Capture", command=self.start_capture)
        self.start_button.pack()

    def start_capture(self):
        self.text_area.delete('1.0', tk.END)  # Clear previous text
        try:
            sniff(iface='br-e55ff388d513', prn=self.packet_handler, count=10)
        except PermissionError:
            messagebox.showerror("Permission Error", "Permission denied. Try running as root or administrator.")

    def packet_handler(self, packet):
        self.text_area.insert(tk.END, packet.summary() + "\n")
        self.text_area.see(tk.END)  # Scroll to the end of the text area


if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()
