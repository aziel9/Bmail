import socket

class SocketConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, message):
        self.socket.sendall(message.encode())
    
    def receive(self):
        return self.socket.recv(4096).decode()
    
    def close(self):
        self.socket.close()

# import socket

# class SocketConnection:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.socket = None
    
#     def connect(self):
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.connect((self.host, self.port))

#     def send(self, message):
#         CHUNK_SIZE = 4096
#         total_sent = 0
#         while total_sent < len(message):
#             chunk = message[total_sent:total_sent+CHUNK_SIZE]
#             sent = self.socket.send(chunk.encode())
#             if sent == 0:
#                 raise RuntimeError("socket connection broken")
#             total_sent += sent
    
#     def receive(self):
#         CHUNK_SIZE = 4096
#         chunks = []
#         while True:
#             chunk = self.socket.recv(CHUNK_SIZE).decode()
#             if not chunk:
#                 break
#             chunks.append(chunk)
#         return ''.join(chunks)
    
#     def close(self):
#         self.socket.close()
