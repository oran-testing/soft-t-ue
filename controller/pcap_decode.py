from scapy.all import Packet, ByteField, PacketField, bind_layers, Raw
from scapy.layers.inet import IP, UDP
from scapy.all import *

class RRC_setup(Packet):
    name = "RRCSetupRequest"
    
    def __init__(self, *args, **kwargs):
        bytes_input = args[0]
        udp_header = UDP(bytes_input[:8])
        kwargs["udp"] = udp_header
        # Process the remaining bytes as needed
        remaining_payload = bytes_input[8:]
        kwargs["payload"] = Raw(load=remaining_payload)
        super().__init__(*args, **kwargs)

    fields_desc = [
        PacketField("udp", None, UDP),  # Use UDP() as the first field in the custom packet
        # Additional fields can be added here
        ByteField("payload", None),     # Add a placeholder for the payload
    ]

packets = rdpcap('ue_mac_nr.pcap')

test = RRC_setup(bytes(packets[0]))
print(test.show())
