

# import tkinter as tk
# from PIL import Image, ImageTk, ImageOps, ImageDraw

# root = tk.Tk()

# frame_path = "frame.png"
# frame_img = Image.open(frame_path)

# img_path = "camera.jpg"
# img = Image.open(img_path)
# img = img.resize((200, 200), resample=Image.LANCZOS)

# mask = Image.new("L", (200,200), 0)
# draw = ImageDraw.Draw(mask)
# draw.ellipse((0, 0, 200, 200), fill=255)
# img.putalpha(mask)


# rounded_img = ImageOps.fit(img, (185, 185), method=Image.LANCZOS)


# frame_img.paste(rounded_img, (7, 7), rounded_img)

# photo = ImageTk.PhotoImage(frame_img)

# frame_label = tk.Label(root, image=photo)
# frame_label.pack()
# root.mainloop()



import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageDraw
from io import BytesIO

root = tk.Tk()

frame_path = "frame.png"
frame_img = Image.open(frame_path)

with open ('camera.jpg','rb') as f:
    image_bytes = f.read()

img = Image.open(BytesIO(image_bytes))
img = img.resize((200, 200), resample=Image.LANCZOS)

mask = Image.new("L", (200,200), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 200, 200), fill=255)
img.putalpha(mask)

rounded_img = ImageOps.fit(img, (185, 185), method=Image.LANCZOS)


frame_img.paste(rounded_img, (7, 7), rounded_img)

photo = ImageTk.PhotoImage(frame_img)

frame_label = tk.Label(root, image=photo)
frame_label.pack()
root.mainloop()

