import socket
from server import active_peers

def connect_to_peers():
    """Connects to active peers and sends a greeting message."""
    for peer in list(active_peers):  # Convert to list to avoid runtime modification issues
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer[0], peer[1]))
            sock.send("Hello, I'm now connected!".encode())
            sock.close()
            print(f"Connected to {peer[0]}:{peer[1]}")
        except:
            print(f"Could not connect to {peer[0]}:{peer[1]}")