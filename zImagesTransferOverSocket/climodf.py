import socket
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()

def upload_image():
    # file_path = filedialog.askopenfilename()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    filename, file_extension = os.path.splitext(os.path.basename(file_path))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(('localhost', 1234))
    client_socket.connect(('100.108.66.28',1234))

    with open(file_path, 'rb') as f:
        image_bytes = f.read()

    metadata = f"{filename}|{file_extension}".encode()
    data = b"".join([metadata, b":", image_bytes])
    client_socket.sendall(data)
    # client_socket.sendaall(data)

    client_socket.close()
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

root.mainloop()