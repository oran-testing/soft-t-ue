from scapy.all import Packet, PacketField, Raw
from scapy.layers.inet import UDP
from scapy.all import rdpcap
from visualize import packet_to_canvas, write_to_pdf
import hexdump
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

buffer = bytes(packets[4])[37:63]

# Binary strings

test = "01111110000000000100000101111001000000000000110100000001000000001111"
test2 = "0001000000000000000001011101111110000000000100000101111001000000000000110100000001000000001111000100010000000000000000000000000000000000000001000000110010010101000111011000001000001011100000001011110000011100"


def bytes_to_binary(byte_obj):
    """Convert a bytes object to a binary string."""
    return ''.join(f'{byte:08b}' for byte in byte_obj)

def binary_to_bytes(binary_str):
    """Convert a binary string to a bytes object."""
    return int(binary_str, 2).to_bytes((len(binary_str) + 7) // 8, byteorder='big')

def extract_bits(byte_obj, start_bit, end_bit):
    """Extract bits from start_bit to end_bit from a bytes object."""
    # Convert bytes to binary string
    binary_str = bytes_to_binary(byte_obj)
    
    # Extract the desired bits
    extracted_bits = binary_str[start_bit:end_bit]
    
    # Convert the extracted bits back to bytes
    extracted_bytes = binary_to_bytes(extracted_bits)
    
    return extracted_bits, extracted_bytes

def shift_bits_left(binary_str, shift_amount):
    """Shift the binary string left by the specified amount of bits."""
    # Perform the shift operation
    shifted_binary_str = binary_str[shift_amount:]  # Remove shifted bits on the left
    # Pad with zeros on the right to maintain original length
    shifted_binary_str = shifted_binary_str.ljust(len(binary_str), '0')
    return shifted_binary_str

def shift_bytes_left(byte_obj, shift_amount):
    """Shift bytes left by the specified number of bits."""
    # Convert bytes to binary string
    binary_str = bytes_to_binary(byte_obj)
    
    # Shift the binary string left
    shifted_binary_str = shift_bits_left(binary_str, shift_amount)
    
    # Convert the shifted binary string back to bytes
    shifted_bytes = binary_to_bytes(shifted_binary_str)
    
    return shifted_bytes

extracted_bits, extracted_bytes = extract_bits(buffer, 27, 202)

new_bytes = shift_bytes_left(extracted_bytes, 4)

print(hexdump.dump(extracted_bytes))

