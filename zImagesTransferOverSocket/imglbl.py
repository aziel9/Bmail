from PIL import Image, ImageTk, ImageDraw, ImageOps
from io import BytesIO

# file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
# if not file_path:
#     return
# filename, file_extension = os.path.splitext(os.path.basename(file_path))
# with open(file_path, 'rb') as f:
#     img_bytes = f.read()
# resize_image = Image.open(BytesIO(img_bytes))
# rimage = resize_image.resize((200, 200), resample=Image.LANCZOS)
# img_bytes = BytesIO()
# try:
#     rimage.save(img_bytes, format='JPEG')
# except:
#     rimage.save(img_bytes, format='PNG')
# img_bytes = img_bytes.getvalue()

mypic = Image.open("frame.png")

with open('camera.jpg', 'rb') as f:
    img_bytes = f.read()
pimage = Image.open(BytesIO(img_bytes))
pimage = pimage.resize((200, 200), resample=Image.LANCZOS)

mask = Image.new("L", (200,200), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 200, 200), fill=255)
pimage.putalpha(mask)

rimage = ImageOps.fit(pimage, (185, 185), method=Image.LANCZOS)
img_bytes = BytesIO()
try:
    # rimage.save(img_bytes, format='JPEG')
    rimage.save("test.jpg", format='JPEG')
except BaseException as msg:
    rimage.save("test.png", format='PNG')
    # rimage.save(img_bytes, format='PNG')
img_bytes = img_bytes.getvalue()
# mypicdisplay_img.paste(rounded_img, (7, 7), rounded_img)