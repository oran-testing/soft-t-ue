from scapy.all import Packet, PacketField, Raw
from scapy.layers.inet import UDP
from scapy.all import rdpcap
from visualize import packet_to_canvas, write_to_pdf
from utils import *
import hexdump
import sys

class RRCSetupRequest(Packet):
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

class DedicatedNASMessage(Packet):
    name = "DedicatedNASMessage"
    
    fields_desc = [
        PacketField("protocol", Raw(), Raw),
        PacketField("message_type", Raw(), Raw),
        PacketField("NAS_key_id", Raw(), Raw),
        PacketField("imsi", Raw(), Raw),
        PacketField("security_capability", Raw(), Raw),
    ]
    
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            _, extracted_bytes = extract_bits(args[0], 27, 202)
            extracted_bytes += b'\x70'
            kwargs["protocol"] = Raw(load=extracted_bytes[0:1])
            kwargs["message_type"] = Raw(load=extracted_bytes[1:3])
            kwargs["NAS_key_id"] = Raw(load=extracted_bytes[3:4])
            kwargs["imsi"] = Raw(load=extracted_bytes[4:19])
            kwargs["security_capability"] = Raw(load=extracted_bytes[19:23])
        super().__init__(*args, **kwargs)


class RRCConnectionRequest(Packet):
    name = "RRCConnectionRequest"
    
    fields_desc = [
        PacketField("udp", UDP(), UDP),
        PacketField("inter", Raw(), Raw),
        PacketField("lcid", Raw(), Raw),
        PacketField("sdu_len", Raw(), Raw),
        PacketField("DedicatedNAS", DedicatedNASMessage(), DedicatedNASMessage),
        PacketField("footer", Raw(), Raw),
    ]
    
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            bytes_input = args[0]
            udp_header = UDP(bytes_input[:8])
            kwargs["udp"] = udp_header
            kwargs["inter"] = Raw(load=bytes_input[8:31])
            kwargs["lcid"] = Raw(load=bytes_input[31:32])
            kwargs["sdu_len"] = Raw(load=bytes_input[32:33])
            kwargs["DedicatedNAS"] = DedicatedNASMessage(bytes_input[37:63])
            kwargs["footer"] = Raw(load=bytes_input[60:72])
        super().__init__(*args, **kwargs)


packets = rdpcap('ue_mac_nr.pcap')

test = RRCConnectionRequest(bytes(packets[4]))

print(test.show())
write_to_pdf(packet_to_canvas(test.DedicatedNAS, rebuild=0),"./test.pdf")

