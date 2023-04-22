import time
import threading
import socket

class SocketConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.is_connected =  False
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.is_connected = True
    
    def send(self, message):
        self.socket.send(message.encode())
    
    def receive(self):
        return self.socket.recv(1024).decode()

socket_connection = SocketConnection("localhost", 1234)

def check_connection():
    global socket_connection
    while True:
        try:
            if not socket_connection.socket:
                socket_connection.connect()
                print("Connected to server!")
        except:
            print("Error: Could not connect to server!")
        time.sleep(5) # check connection every 1 minute

# start the thread to check connection
thread = threading.Thread(target=check_connection)
thread.start()
