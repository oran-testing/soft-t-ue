from scapy.all import Packet, PacketField, Raw
from scapy.layers.inet import UDP
from scapy.all import rdpcap
from visualize import packet_to_canvas, write_to_pdf
from pyasn1.codec.ber.decoder import decode
from pyasn1.type.univ import OctetString
import hexdump
from pyasn1.type import univ
from pyasn1.type import char
from pyasn1.type import namedtype
from pyasn1.type import constraint
from pyasn1.type import tag
from pyasn1.type import useful
import asn1tools

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

# Create a test packet and show its details
#test = RRC_setup(bytes(packets[0]))
#print(test.show())

#write_to_pdf(packet_to_canvas(test), "./test.pdf")
#write_to_pdf(packet_to_canvas(packets[4]), "./rrc_registration.pdf")
#print(hexdump.dump(bytes(packets[4])[37:63]))
#print(hexdump.dump(bytes(packets[4])[39:37 + 23]))
#decoded_message, _ = decode(bytes(packets[4])[37:63], asn1Spec=NASMessage())

dcch_decoder = asn1tools.compile_files("./rrc_8_6_0.asn")
buffer = bytearray(bytes(packets[4])[37:63])
buffer[0] = 0x30
print(hexdump.dump(buffer))
print(hexdump.dump(dcch_decoder.decode('RRCSetupComplete-IEs',buffer)))



