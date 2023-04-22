import socket

# Load image data from file
with open("camera.jpg", "rb") as f:
    image_data = f.read()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
# server_socket.bind(('100.108.66.28',1234))
server_socket.listen()

while True:
    client_socket, address = server_socket.accept()
    request = client_socket.recv(1024)

    if request == b"get_image":
        client_socket.sendall(image_data)

    client_socket.close()
