from scapy.all import Packet, PacketField, Raw, rdpcap, ByteField, RawVal, StrLenField
from scapy.layers.inet import UDP

from utils import extract_bits
from visualize import packet_to_canvas, write_to_pdf


class RRCSetupRequest(Packet):
    name = "RRCSetupRequest"

    fields_desc = [
        PacketField("udp", UDP(), UDP),
        PacketField("payload", Raw(), Raw),
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
            extracted_bytes += b"\x70"
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
        StrLenField('inter', b''),
        ByteField("lcid", 0),
        ByteField("sdu_len", 0),
        PacketField("DedicatedNAS", DedicatedNASMessage(), DedicatedNASMessage),
        StrLenField("footer", b''),
    ]

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            bytes_input = args[0]
            udp_header = UDP(bytes_input[:8])
            kwargs["udp"] = udp_header
            kwargs["inter"] = bytes_input[8:31]
            kwargs["lcid"] = int.from_bytes(bytes_input[31:32], byteorder='big')
            kwargs["sdu_len"] = int.from_bytes(bytes_input[32:33], byteorder='big')
            kwargs["DedicatedNAS"] = DedicatedNASMessage(bytes_input[37:63])
            kwargs["footer"] = load=bytes_input[60:72]
        super().__init__(*args, **kwargs)


packets = rdpcap("ue_mac_nr.pcap")

test = RRCConnectionRequest(bytes(packets[4]))

print(test.show())
write_to_pdf(packet_to_canvas(test, rebuild=0), "./test.pdf")
