##libraries
import socket
import threading

HOST = "172.16.60.142" # enter your ip address here
PORT = 10000

clients = {} ## dictionary for the clients names to their socket connections
lock = threading.Lock() 

def broadcast_active_clients():## sends an updated list of active client names to all connected clients
    with lock:
        client_list = list(clients.keys())
        msg = f"ACTIVE_CLIENTS:{','.join(client_list)}"
        for conn in clients.values():
            try:
                conn.sendall(msg.encode('utf-8'))
            except:
                pass

def broadcast_message(message):##sends a message to all the clients
    with lock:
        for conn in clients.values():
            try:
                conn.sendall(message.encode('utf-8'))
            except:
                pass

def handle_client(conn, addr): ##handles client connection, username, and incoming messages
    name=None ##client name is None until received a diffrent name from client

    try:
        conn.sendall("Enter your name: ".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8').strip()

        with lock: ##enters client to client dictionry
            clients[name] = conn
        print(f"{name} connected from {addr}")
        conn.sendall(f"Welcome {name}! You can now send messages Use: to:client;message.\n".encode('utf-8'))
        
        # updates all about a new client 
        broadcast_message(f"{name} has joined the chat!")
        broadcast_active_clients()

        while True:
            data = conn.recv(1024)
            if not data:
                break

            data_str = data.decode('utf-8')

            if data_str.startswith("to:"):##if the message starts with to:
                try:
                    target_name, msg = data_str[3:].split(";", 1)
                    target_name = target_name.strip()
                    msg=msg.strip()
                except ValueError:
                    conn.sendall("Invalid message format.(Use: to:client;message)".encode('utf-8')) 
                    continue

                with lock:##sends appropreate message according to the info recived from the client
                    if target_name in clients:
                        clients[target_name].sendall(f"From {name}: {msg}".encode('utf-8'))
                        conn.sendall(f"Message sent successfully to: {target_name}.".encode('utf-8'))
                    else:
                        conn.sendall(f"User {target_name} not online.".encode('utf-8'))
            else:
                conn.sendall("Invalid message format (Use: to:client;message)".encode('utf-8')) 

    except ConnectionResetError: ##if there were any disconnection
        if name: 
            print(f"{name} disconnected from {addr} ") 
        else: 
            print(f"{addr} disconnected")
    finally:
        with lock:
            if name in clients:
                del clients[name]
        conn.close()
        # updates about dissconection
        if name:
            broadcast_message(f"{name} has left the chat!")
        broadcast_active_clients()

def start_server():##function to start the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active clients: {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()