import tkinter as tk
from PIL import ImageTk, Image, ImageDraw

# Create a Tkinter window
root = tk.Tk()

# Load the image
img_path = r"camera.jpg"
img = Image.open(img_path)

# Resize the image
img = img.resize((200, 200), resample=Image.LANCZOS)

# Make the image rounded
mask = Image.new('L', (200, 200), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 200, 200), fill=255)
img.putalpha(mask)

# Convert the image to a Tkinter PhotoImage
photo = ImageTk.PhotoImage(img)

# Create a Tkinter label and display the image
label = tk.Label(root, image=photo)
label.pack()

# Run the Tkinter event loop
root.mainloop()
