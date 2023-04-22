import socket
import json

class SocketConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_large_data(self, data):
        request_json = json.dumps(data)
        request_bytes = request_json.encode()
        chunk_size = 1024
        num_chunks = len(request_bytes) // chunk_size + 1
        request = {'type': 'large_data', 'num_chunks': num_chunks}
        self.socket.sendall(json.dumps(request).encode())
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size
            self.socket.sendall(request_bytes[start:end])

    def receive_large_data(self):
        response = ''
        while True:
            data = self.socket.recv(1024).decode()
            response += data
            if not data:
                break
        return json.loads(response)

    def close(self):
        self.socket.close()

# Sample usage
data = {'email': 'abc@gmail.com', 'password': 'abc123'}
conn = SocketConnection('localhost', 8080)
conn.connect()
conn.send_large_data(data)
response = conn.receive_large_data()
print(response)
conn.close()
