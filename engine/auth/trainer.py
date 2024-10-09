import platform
import cv2
import numpy as np
from PIL import Image #pillow package
import os

if platform.system() == 'Darwin':
    path = 'engine/auth/samples' # Path for samples already taken
elif platform.system() == 'Windows':
    path = 'engine\\auth\\samples' # Path for samples already taken
else:
    print("This is another OS")

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms

#Haar Cascade classifier is an effective object detection approach
if platform.system() == 'Darwin':
    detector = cv2.CascadeClassifier("engine/auth/haarcascade_frontalface_default.xml")
elif platform.system() == 'Windows':
    detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
else:
    print("This is another OS")

def Images_And_Labels(path): # function to fetch the images and labels

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths: # to iterate particular image path

        gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_arr = np.array(gray_img,'uint8') #creating an array

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            faceSamples.append(img_arr[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("Training faces. It will take a few seconds. Wait ...")

faces,ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

if platform.system() == 'Darwin':
    recognizer.write('engine/auth/trainer/trainer.yml')  # Save the trained model as trainer.yml
elif platform.system() == 'Windows':
    recognizer.write('engine\\auth\\trainer\\trainer.yml')  # Save the trained model as trainer.yml
else:
    print("This is another OS")

print("Model trained, Now we can recognize your face.")