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
        self.socket.send(message.encode())
    
    def receive(self):
        return self.socket.recv(1024).decode()

class Signin:
    activeusr_name = None
    activeusr_email = None
    
    def __init__(self, window, socket_connection):
        self.window = window
        self.socket_connection = socket_connection
        # ... rest of the code
    
    def validation(self):
        try:
            if self.email_entry.get() == "":
                messagebox.showerror("Error", "Please enter email id")
            elif self.password_entry.get()=="":
                messagebox.showerror("Error", "Please enter password")
            elif self.is_valid_email() is False:
                messagebox.showerror("Error", "Invalid email format")
            else:
                self.login()
        except BaseException as msg:
            messagebox.showerror("Empty Field","Enter all the fields")
            print(msg)
    
    def login(self):
        try:
            email= self.email_entry.get()
            password= self.password_entry.get()
            self.socket_connection.send(f"login|{email}|{password}")
            response = self.socket_connection.receive()
            if response == "Incorrect email":
                messagebox.showerror("Error", "Invalid Email id")
            elif response == "Incorrect password":
                messagebox.showerror("Error", "Invalid password")
            else:
                # login successful, do something
                pass
        except socket.error as msg:
            # handle socket error
            pass

# create an instance of the SocketConnection class
socket_connection = SocketConnection("localhost", 1234)
socket_connection.connect()

# create an instance of the Signin class and pass the socket_connection instance to it
window = Tk()
signin = Signin(window, socket_connection)

window.mainloop()
