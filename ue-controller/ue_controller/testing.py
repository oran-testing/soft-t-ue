from scapy.all import Packet, PacketField, Raw
from scapy.layers.inet import UDP
from scapy.all import rdpcap
from visualize import packet_to_canvas, write_to_pdf
from utils import *
import hexdump
import asn1tools
import sys

class RRC_setup(Packet):
    name = "RRCSetupRequest"
    
    fields_desc = [
        PacketField("udp", UDP(), UDP),
        PacketField("payload", Raw(), Raw)  # Use Raw for handling raw byte data
    ]
    
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            bytes_input = args[0]
            udp_header = UDP(bytes_input[:8])
            kwargs["udp"] = udp_header
            remaining_payload = bytes_input[8:]
            kwargs["payload"] = Raw(load=remaining_payload)
        super().__init__(*args, **kwargs)

# Load packets from pcap file
packets = rdpcap('ue_mac_nr.pcap')

buffer = bytes(packets[4])[37:63]

extracted_bits, extracted_bytes = extract_bits(buffer, 27, 202)

new_bytes = shift_bytes_left(extracted_bytes, 12)


decoder = asn1tools.compile_files(sys.argv[1])

another_buffer = bytearray(shift_bytes_left(bytes(packets[1]), 4))[20:]
print(hexdump.dump(another_buffer))

new_buffer = new_bytes + b'\x70\x00\x00'
print(hexdump.dump(new_bytes))

decoded_data = decoder.decode('DedicatedNAS-Message', new_buffer)
print(decoded_data)

