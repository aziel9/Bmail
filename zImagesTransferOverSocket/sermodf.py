import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('localhost', 1234))
server_socket.bind(('100.83.45.111',1234))
server_socket.listen()

client_socket, address = server_socket.accept()

data = b''
while True:
    chunk = client_socket.recv(4096)
    if not chunk:
        break
    data += chunk

metadata, image_data = data.split(b':',1)

filename, file_extension = metadata.decode().split('|')
# filename = filename+file_extension
filename = f"{filename}test"

with open(f'images\\{filename}{file_extension}', 'wb') as f:
    f.write(image_data)

print(f'images\\{filename}{file_extension}')
client_socket.close()
server_socket.close()
