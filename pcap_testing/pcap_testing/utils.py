import subprocess

def start_subprocess(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def kill_subprocess(process):
    process.terminate()  # Graceful termination
    try:
        process.wait(timeout=5) 
    except subprocess.TimeoutExpired:
        process.kill()  # Forceful termination
    process.communicate()

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


