import tkinter as tk
import io
from PIL import Image, ImageTk
import socket

root = tk.Tk()

def request_image():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))
    # client_socket.connect(('100.108.66.28',1234))

    # Send request for image data
    client_socket.sendall(b"get_image")

    # Receive image data and create ImageTk object
    image_data = b""
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        image_data += chunk
    image = Image.open(io.BytesIO(image_data))
    image_tk = ImageTk.PhotoImage(image)

    # Display image in tkinter window
    label = tk.Label(root, image=image_tk)
    label.image = image_tk  # Need to keep a reference to the image object
    label.pack()

    client_socket.close()

request_button = tk.Button(root, text="Request Image", command=request_image)
request_button.pack()

root.mainloop()
