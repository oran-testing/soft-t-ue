from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
import sys
from scapy.all import *


class PacketSniffer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Packet Sniffer')
        self.setGeometry(100, 100, 800, 600)

        # Text edit to display captured packets
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Start button to begin packet capture
        self.start_button = QPushButton('Start Capture')
        self.start_button.clicked.connect(self.start_capture)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.start_button)

        # Main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

    def start_capture(self):
        self.text_edit.clear()
        sniff(iface='br-e55ff388d513', prn=self.packet_handler, count=100)

    def packet_handler(self, packet):
        print(packet.summary())
        self.text_edit.append(packet.summary())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PacketSniffer()
    window.show()
    sys.exit(app.exec_())
