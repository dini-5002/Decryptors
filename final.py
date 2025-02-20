import socket
import threading
import time

active_peers = {}  # Maps peer IP to their listening port
received_from = set()  # Tracks peers from whom messages were received
active_connections = {}  # Stores active socket connections

MANDATORY_PEERS = [
    ("10.206.5.228", 6555)
]

def handle_client(client_socket, client_address):
    try:
        sender_port_data = client_socket.recv(1024).decode().strip()
        data_parts = sender_port_data.split("\n", 1)
        sender_port = int(data_parts[0]) if data_parts[0].isdigit() else None

        if sender_port:
            active_peers[client_address[0]] = sender_port
            received_from.add((client_address[0], sender_port))
            print(f"🔵 Connected to {client_address[0]}:{sender_port}")

            if len(data_parts) > 1:
                message = data_parts[1].strip()
                print(f"📩 Received from {client_address[0]}:{sender_port}: {message}")
                client_socket.sendall(f"✅ Message received".encode())

        while True:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                continue
            
            if message.lower() == "exit":
                print(f"🔴 Client {client_address[0]}:{sender_port} disconnected.")
                active_connections.pop((client_address[0], sender_port), None)
                break
            
            received_from.add((client_address[0], sender_port))
            print(f"📩 Received from {client_address[0]}:{sender_port}: {message}")
            client_socket.sendall(f"✅ Message received".encode())

    except Exception as e:
        print(f"⚠️ Connection error with {client_address[0]}: {e}")
    finally:
        client_socket.close()

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    print(f"Server listening on {ip}:{port}...")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def query_peers():
    print("\nConnected Peers:")
    if received_from:
        for ip, port in received_from:
            status = "Active" if (ip, port) in active_connections else "Inactive"
            print(f"{ip}:{port} - {status}")
    else:
        print("No connected peers")

def connect_to_peer(ip, port, my_port):
    try:
        if (ip, port) not in active_connections:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            client_socket.sendall(f"{my_port}\nCONNECT\n".encode())
            active_connections[(ip, port)] = client_socket
            received_from.add((ip, port))
            print(f"✅ Successfully connected to {ip}:{port}")
        else:
            print(f"Already connected to {ip}:{port}")
    except Exception as e:
        print(f"❌ Error connecting to {ip}:{port} - {e}")

def connect_to_active_peers(my_port):
    print("\n🔄 Connecting to known peers...\n")
    for ip, port in list(received_from):
        if (ip, port) not in active_connections:
            connect_to_peer(ip, port, my_port)
    
    if not received_from:
        print("No known peers to connect to.")
    else:
        print("Finished connecting to known peers.")

def send_message(ip, port, my_port):
    if (ip, port) not in active_connections:
        connect_to_peer(ip, port, my_port)
    
    if (ip, port) in active_connections:
        conn = active_connections[(ip, port)]
        while True:
            message = input("Enter message (type 'exit' to disconnect, 'menu' for options): ").strip()
            if message.lower() == 'menu':
                break
            elif message.lower() == "exit":
                conn.close()
                active_connections.pop((ip, port), None)
                print(f"🔴 Disconnected from {ip}:{port}")
                break
            try:
                conn.sendall(f"{message}\n".encode())
                ack = conn.recv(1024).decode().strip()
                print(f"✅ Acknowledgment from {ip}:{port} - {ack}")
            except Exception as e:
                print(f"❌ Error sending message to {ip}:{port} - {e}")
                conn.close()
                active_connections.pop((ip, port), None)
                break
    else:
        print(f"❌ Not connected to {ip}:{port}")

def send_mandatory_messages(my_port):
    for ip, port in MANDATORY_PEERS:
        try:
            connect_to_peer(ip, port, my_port)
            if (ip, port) in active_connections:
                conn = active_connections[(ip, port)]
                conn.sendall(f"Auto Message\n".encode())
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
            if not active_connections:
                recipient_ip = input("Enter recipient's IP: ")
                recipient_port = int(input("Enter recipient's Port: "))
            else:
                print("Active connections:")
                for i, (ip, port) in enumerate(active_connections.keys(), 1):
                    print(f"{i}. {ip}:{port}")
                choice = int(input("Choose a connection (0 for new): "))
                if choice == 0:
                    recipient_ip = input("Enter recipient's IP: ")
                    recipient_port = int(input("Enter recipient's Port: "))
                else:
                    recipient_ip, recipient_port = list(active_connections.keys())[choice - 1]
            send_message(recipient_ip, recipient_port, port)
        elif choice == "2":
            query_peers()
        elif choice == "3":
            connect_to_active_peers(port)
        elif choice == "0":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
