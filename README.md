# P2P Chat System

## Overview
This is a decentralized Peer-to-Peer (P2P) chat system that allows users to communicate directly without relying on a central server. The system enables multiple peers to connect, send messages, and maintain an active connection network.

## Features
- Peer-to-peer communication without a central server
- Automatic connection to mandatory peers
- Querying of active peers
- Handling of message acknowledgments
- Graceful disconnection management

## Project Structure
```
|-- final.py       # Main P2P chat application
|-- client.py      # Simple message sender
|-- server.py      # Handles incoming connections and messages
|-- utils.py       # Utility functions for connecting to peers
```

## Requirements
- Python 3.x
- Socket and Threading libraries (built-in)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/p2p-chat.git
   cd p2p-chat
   ```

2. Ensure Python 3 is installed.
3. No additional dependencies are required.

## Usage

### Running the P2P Chat Application

1. Start the chat application:

   ```sh
   python final.py
   ```

2. Enter your details when prompted:

   - Team name
   - IP Address
   - Port Number

3. Use the menu options to:

   - Send messages
   - Query active peers
   - Connect to known peers

### Running as a Simple Client

To send a message from a standalone client:

```sh
python client.py
```

Modify the script to provide the desired IP, port, and message.

### Running as a Server

To start a standalone server:

```sh
python server.py
```

The server will listen for incoming messages and handle peer connections.

### Connecting to Peers

To manually connect to a peer:

```sh
python utils.py
```

This will attempt to connect to known active peers.

## Configuration

### Mandatory Peers

You can modify the `MANDATORY_PEERS` list in `final.py` to include default peers that should always be connected at startup.

## Known Issues & Improvements

- Improve peer discovery mechanism.
- Enhance disconnection handling.
- Implement encryption for secure messaging.


