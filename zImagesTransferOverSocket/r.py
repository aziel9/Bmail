import cv2
import numpy as np

# Load the image
img = cv2.imread(r'C:\Users\dpace\OneDrive\Desktop\New Email\zImagesTransferOverSocket\lady.jpg')

# Resize the image to 100x100 keeping the aspect ratio
img_size = 400
h, w = img.shape[:2]
if h > w:
    new_h, new_w = img_size, int(w * img_size / h)
else:
    new_h, new_w = int(h * img_size / w), img_size
img = cv2.resize(img, (new_w, new_h))

# Create a black mask with a white circle
mask = np.zeros((new_h, new_w, 3), np.uint8)
cx, cy = new_w//2, new_h//2
radius = min(new_h, new_w) // 2
cv2.circle(mask, (cx, cy), radius, (255, 255, 255), -1)

# Apply the mask to the image
img_round = cv2.bitwise_and(img, mask)

# Show the original and rounded image
cv2.imshow('Original Image', img)
cv2.imshow('Rounded Image', img_round)
cv2.waitKey(0)
cv2.destroyAllWindows()
