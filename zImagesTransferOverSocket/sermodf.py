import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('localhost', 1234))
server_socket.bind(('100.108.66.28',1234))
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
filename = filename+file_extension


with open(f'{filename}{file_extension}', 'wb') as f:
    f.write(image_data)


client_socket.close()
server_socket.close()
