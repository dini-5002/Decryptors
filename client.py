import socket

def send_message(ip, port, message):
    """Sends a message to a given peer."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        client_socket.send(message.encode())
        client_socket.close()
        print(f"Message sent to {ip}:{port}")
    except:
        print(f"Failed to send message to {ip}:{port}")