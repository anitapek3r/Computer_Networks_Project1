import socket
import threading

HOST = "172.16.60.142" #enter your ip address
PORT = 10000

class Client: ##class that represents chat client to server
    def __init__(self, name, on_message_callback, on_clients_update_callback):
        self.name = name
        self.on_message_callback = on_message_callback
        self.on_clients_update_callback = on_clients_update_callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self): ##connect the client to the server
        try:
            self.sock.connect((HOST, PORT))
            self.sock.recv(1024)
            self.sock.sendall(self.name.encode('utf-8'))

            self.connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()

            return f"Connected as {self.name}"
        except Exception as e:
            return f"Connection failed: {e}"

    def receive_messages(self):## receives messages from the server
        while self.connected:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if not msg:
                    break

                msg = msg.strip()

                if msg.startswith("ACTIVE_CLIENTS:"):
                    client_list = msg[15:].split(',')
                    client_list = [c.strip() for c in client_list if c.strip()]
                    self.on_clients_update_callback(client_list)
                else:

                    self.on_message_callback(msg)
            except:
                break
        self.connected = False

    def send_message(self, msg): ##send a message to the server if the client is connected
        if self.connected:
            try:
                self.sock.sendall(msg.encode('utf-8'))
            except:
                self.connected = False

    def disconnect(self): ## disconnects the client and closes the socket
        self.connected = False
        try:
            self.sock.close()
        except:
            pass