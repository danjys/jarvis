import cv2

img = cv2.imread('testpy/image.jpg')
if img is None:
    print("Image not loaded. Check the path or file permissions.")
else:
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("Image successfully converted.")
