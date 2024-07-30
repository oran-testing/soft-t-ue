from scapy.all import Packet, PacketField, Raw, rdpcap, ByteField, RawVal, StrLenField, BitField
from scapy.layers.inet import UDP

from utils import extract_bits
from visualize import packet_to_canvas, write_to_pdf


class RRCSetupRequest(Packet):
    name = "RRCSetupRequest"

    fields_desc = [
        PacketField("udp", UDP(), UDP),
        StrLenField("message_type",b''),
        ByteField("radio_type",0),
        ByteField("message_direction",0),
        StrLenField("padding_a", 0),
        BitField("RNTI",0, 16),
        ByteField("C_RNTI",0),
        StrLenField("padding_b", 0),
        ByteField("HarqId",0),
        StrLenField("padding_c", 0),
        ByteField("reserved",0),
        ByteField("LCID", 0),
        ByteField("serving_cell_id", 0),
        ByteField("coreset_id", 0),
        ByteField("tci_state_id", 0),
        ByteField("reserved_b", 0),
        ByteField("resource_set_activation", 0),
        PacketField("payload", Raw(), Raw),
    ]

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            bytes_input = args[0]
            udp_header = UDP(bytes_input[:8])
            kwargs["udp"] = udp_header
            kwargs["message_type"] = bytes_input[8:14]
            kwargs["radio_type"] = int.from_bytes(bytes_input[14:15], byteorder='big')
            kwargs["message_direction"] = int.from_bytes(bytes_input[15:16], byteorder='big')
            kwargs["padding_a"] = bytes_input[16:18]
            kwargs["RNTI"] = int.from_bytes(bytes_input[18:20], byteorder='big')
            kwargs["C_RNTI"] = int.from_bytes(bytes_input[20:21], byteorder='big')
            kwargs["padding_b"] = bytes_input[21:24]
            kwargs["HarqId"] = int.from_bytes(bytes_input[24:25], byteorder='big')
            kwargs["padding_c"] = bytes_input[25:30]
            kwargs["reserved"] = int.from_bytes(bytes_input[30:31], byteorder='big') & 0b11
            kwargs["LCID"] = int.from_bytes(bytes_input[30:31], byteorder='big') & 0b00111111
            kwargs["serving_cell_id"] = int.from_bytes(bytes_input[31:32], byteorder='big') & 0b11111
            kwargs["coreset_id"] = int.from_bytes(bytes_input[31:33], byteorder='big') & 0b00000111
            kwargs["tci_state_id"] = int.from_bytes(bytes_input[32:33], byteorder='big') & 0b000001111
            kwargs["reserved_b"] = int.from_bytes(bytes_input[33:34], byteorder='big') & 0b11
            kwargs["resource_set_activation"] = int.from_bytes(bytes_input[33:34], byteorder='big') & 0b00111111
            kwargs["payload"] = Raw(load=bytes_input[33:])
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
#test = RRCConnectionRequest(bytes(packets[4]))
test = RRCSetupRequest(bytes(packets[0]))

print(test.show())
write_to_pdf(packet_to_canvas(test, rebuild=0), "./test.pdf")
