import socket
import threading

active_peers = set()  # Stores connected peers
# this was using ephemeril port

def handle_client(client_socket, client_address):
    """Handles incoming messages and keeps the connection open."""
    active_peers.add(client_address)
    print(f"🔵 Connected to {client_address}")

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message or message.lower() == "exit":
                print(f"🔴 Client {client_address} disconnected.")
                active_peers.remove(client_address)
                break

            print(f"\n📩 Received from {client_address}: {message}")
            client_socket.send("Message received!".encode())  # Send acknowledgment

    except Exception as e:
        print(f"⚠️ Connection error with {client_address}: {e}")

    finally:
        client_socket.close()
def start_server(port):
    """Starts the server to receive messages."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))  # Bind to all available interfaces
    server_socket.listen(5)

    print(f"Server listening on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def query_peers():
    """Displays the list of active peers."""
    print("\nConnected Peers:")
    if active_peers:
        for peer in active_peers:
            print(f"{peer[0]}:{peer[1]}")
    else:
        print("No connected peers")