import socket
import tkinter as tk

# create a socket object
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the IP address of the server
host = "100.108.66.28"

# set the port number
port = 9999

# connect to the server
clientsocket.connect((host, port))

# define button click functions
def send_button_clicked(button_num):
    message = f"Button {button_num} clicked"
    clientsocket.send(message.encode())

# create the tkinter window
root = tk.Tk()

# create the buttons
button1 = tk.Button(root, text='Button 1', command=lambda: send_button_clicked(1))
button2 = tk.Button(root, text='Button 2', command=lambda: send_button_clicked(2))
button3 = tk.Button(root, text='Button 3', command=lambda: send_button_clicked(3))
button4 = tk.Button(root, text='Button 4', command=lambda: send_button_clicked(4))
button5 = tk.Button(root, text='Button 5', command=lambda: send_button_clicked(5))
button6 = tk.Button(root, text='Button 6', command=lambda: send_button_clicked(6))
button7 = tk.Button(root, text='Button 7', command=lambda: send_button_clicked(7))
button8 = tk.Button(root, text='Button 8', command=lambda: send_button_clicked(8))
button9 = tk.Button(root, text='Button 9', command=lambda: send_button_clicked(9))
button10 = tk.Button(root, text='Button 10', command=lambda: send_button_clicked(10))

# place the buttons in the tkinter window
button1.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()
button6.pack()
button7.pack()
button8.pack()
button9.pack()
button10.pack()

def on_closing():
    # close the client socket when the tkinter window is closed
    clientsocket.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# start the tkinter event loop
root.mainloop()
