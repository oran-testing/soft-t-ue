import socket

def send_command(ip, port, command):
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect the socket to the server's IP and port
            sock.connect((ip, port))
            
            # Send the command
            sock.sendall(command.encode('utf-8'))
            print(f"Command '{command}' sent to {ip}:{port}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    ip = "127.0.0.1"
    port = 5000
    command = "5050"

    send_command(ip, port, command)

if __name__ == "__main__":
    main()
