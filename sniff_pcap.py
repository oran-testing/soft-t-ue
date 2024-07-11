from scapy.all import *

def packet_handler(packet):
    print(packet.summary())

# Replace 'eth0' with your network interface name
sniff(iface='br-e55ff388d513', prn=packet_handler, count=100)
