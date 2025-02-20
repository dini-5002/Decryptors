import socket
import threading

active_peers = {}  # Maps peer IP to their listening port
received_from = set()  # Tracks peers from whom messages were received

MANDATORY_PEERS = [
    # ("10.206.4.201", 1255),
    ("10.206.5.228", 6555)
]

def handle_client(client_socket, client_address):
    """Handles incoming messages and keeps the connection open."""
    try:
        sender_port_data = client_socket.recv(1024).decode().strip()
        data_parts = sender_port_data.split("\n", 1)
        sender_port = data_parts[0]

        if sender_port.isdigit():
            sender_port = int(sender_port)
            
            # Ensure multiple connections are tracked
            active_peers[client_address[0]] = sender_port
            received_from.add((client_address[0], sender_port))  # Store (IP, Port) as tuple
            
            print(f"🔵 Connected to {client_address[0]}:{sender_port}")

            if len(data_parts) > 1:
                message = data_parts[1].strip()
                print(f"📩 Received from {client_address[0]}:{sender_port}: {message}")
                client_socket.sendall(f"✅ Message received from {client_address[0]}:{sender_port}".encode())

        while True:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                continue
            
            if message.lower() == "exit":
                print(f"🔴 Client {client_address[0]} disconnected.")
                received_from.discard((client_address[0], sender_port))  # Remove specific entry
                active_peers.pop(client_address[0], None)
                break
            
            received_from.add((client_address[0], sender_port))  # Ensure peer is stored
            print(f"📩 Received from {client_address[0]}:{sender_port}: {message}")
            client_socket.sendall(f"✅ Message received from {client_address[0]}:{sender_port}".encode())

    except Exception as e:
        print(f"⚠️ Connection error with {client_address[0]}: {e}")
    finally:
        client_socket.close()

def start_server(ip, port):
    """Starts the server to receive messages."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    print(f"Server listening on {ip}:{port}...")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def query_peers():
    """Displays the list of all connected peers."""
    print("\nConnected Peers:")
    if received_from:
        for ip, port in received_from:
            print(f"{ip}:{port}")
    else:
        print("No connected peers")


def connect_to_peers():
    """Connects to active peers and sends a handshake message."""
    print("\n🔄 Attempting to connect to known peers...\n")
    
    for ip, port in list(received_from):  # Extract both IP and port
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.sendall("CONNECT\n".encode())

            ack = sock.recv(1024).decode().strip()
            print(f"✅ Successfully connected to {ip}:{port} - Response: {ack}")

            # Ensure the peer is marked as connected
            received_from.add((ip, port))  # Reinforce tracking
            sock.close()

        except socket.timeout:
            print(f"⏳ Timeout connecting to {ip}:{port}")
        except ConnectionRefusedError:
            print(f"🚫 Connection refused by {ip}:{port}")
        except Exception as e:
            print(f"❌ Error connecting to {ip}:{port} - {e}")

def send_message(ip, port, my_port):
    """Sends messages to a peer and keeps the connection open."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.sendall(f"{my_port}\n".encode())

        while True:
            message = input("Enter message (type 'exit' to disconnect): ").strip()
            if message.lower() == "exit":
                break
            client_socket.sendall(f"{my_port}\n{message}\n".encode())
            ack = client_socket.recv(1024).decode().strip()
            print(f"✅ Acknowledgment from {ip}:{port} - {ack}")

        print(f"🔴 Disconnecting from {ip}:{port}")
        client_socket.close()
    except Exception as e:
        print(f"❌ Failed to send message to {ip}:{port} - {e}")

def send_mandatory_messages(my_port):
    """Ensures mandatory messages are sent to required peers."""
    for ip, port in MANDATORY_PEERS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.sendall(f"{my_port}\nAuto Message\n".encode())
            sock.close()
            print(f"✅ Mandatory message sent to {ip}:{port}")
        except Exception as e:
            print(f"❌ Could not send mandatory message to {ip}:{port} - {e}")

def main():
    print("Starting P2P chat application...")
    team_name = input("Enter your team name: ")
    ip = input("Enter your IP address: ")
    port = int(input("Enter your port number: "))

    server_thread = threading.Thread(target=start_server, args=(ip, port))
    server_thread.daemon = True
    server_thread.start()

    send_mandatory_messages(port)

    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")

        choice = input("Enter choice: ")
        if choice == "1":
            recipient_ip = input("Enter recipient's IP: ")
            recipient_port = int(input("Enter recipient's Port: "))
            send_message(recipient_ip, recipient_port, port)
        elif choice == "2":
            query_peers()
        elif choice == "3":
            connect_to_peers()
        elif choice == "0":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()