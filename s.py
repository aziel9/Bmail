import socket

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = "100.108.66.28"

port = 9999

# bind the socket to a public host, and a well-known port
serversocket.bind((host, port))

# become a server socket
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()
    
    # receive data from client
    request_type = clientsocket.recv(1024).decode()
    
    # print response based on request type
    if request_type == 'button_1_clicked':
        print('Button 1 was clicked')
    elif request_type == 'button_2_clicked':
        print('Button 2 was clicked')
    elif request_type == 'button_3_clicked':
        print('Button 3 was clicked')
    elif request_type == 'button_4_clicked':
        print('Button 4 was clicked')
    elif request_type == 'button_5_clicked':
        print('Button 5 was clicked')
    elif request_type == 'button_6_clicked':
        print('Button 6 was clicked')
    elif request_type == 'button_7_clicked':
        print('Button 7 was clicked')
    elif request_type == 'button_8_clicked':
        print('Button 8 was clicked')
    elif request_type == 'button_9_clicked':
        print('Button 9 was clicked')
    elif request_type == 'button_10_clicked':
        print('Button 10 was clicked')
    else:
        print('Invalid request type')

    # close the connection
    clientsocket.close()
