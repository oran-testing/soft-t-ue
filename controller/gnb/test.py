import socket

def main():
    ip = "127.0.0.1"
    port = 5000
    command = "5050"

    send_command(ip, port, command)

if __name__ == "__main__":
    main()
