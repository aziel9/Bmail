import socket
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            c, addr = self.socket.accept()
            request_json = c.recv(1024).decode()
            request_load = json.loads(request_json)
            message = ''
            for i in range(request_load['num_chunks']):
                chunk = c.recv(1024).decode()
                message += chunk
            data = json.loads(message)
            print(f"Received data: {data}")
            response = {'message': 'Data received successfully'}
            c.send(json.dumps(response).encode())
            c.close()

    def stop(self):
        if self.socket is not None:
            self.socket.close()

# Sample usage
server = Server('localhost', 8080)
server.start()
