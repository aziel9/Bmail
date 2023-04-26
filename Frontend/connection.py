import socket
import json

class SocketConnection:
    def __init__(self):
        self.connect()
    
    def connect(self):
        self.host = "100.83.45.111"
        self.port = 1234
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, message):
        request_json = json.dumps(message).encode()
        request_len = len(request_json)
        send_length = request_len.to_bytes(4, byteorder='big')
        self.socket.sendall(send_length)
        self.socket.sendall(request_json)
 
    def receive(self):
        response_len = self.socket.recv(4)
        if response_len:
            response_length = int.from_bytes(response_len, byteorder='big')
            response_json = b''
            while len(response_json) < response_length:
                chunk = self.socket.recv(min(response_length - len(response_json), 1024))
                if not chunk:
                    break
                response_json += chunk
            response = json.loads(response_json.decode())
            return response

    
    def close(self):
        self.socket.close()



# import socket
# import json

# class SocketConnection:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.socket = None
    
#     def connect(self):
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.connect((self.host, self.port))

#     def send(self, message):
#         request_json = json.dumps(message)
#         self.socket.send(request_json.encode())
    
#     def receive(self):
#         response_json = self.socket.recv(4096)
#         response = json.loads(response_json.decode())
#         return response
    
#     def close(self):
#         self.socket.close()

