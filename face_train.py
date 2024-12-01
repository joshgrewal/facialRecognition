import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Path for face image database
dataset_path = "dataset"

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        if not image_path.endswith(".jpg"):
            continue

        pil_image = Image.open(image_path).convert("L")  # Convert to grayscale
        image_np = np.array(pil_image, "uint8")
        id_ = int(os.path.split(image_path)[-1].split(".")[1])
        faces = face_cascade.detectMultiScale(image_np)

        for (x, y, w, h) in faces:
            face_samples.append(image_np[y:y+h, x:x+w])
            ids.append(id_)

    return face_samples, ids

print("Training faces. It will take a few seconds...")
faces, ids = get_images_and_labels(dataset_path)
recognizer.train(faces, np.array(ids))

recognizer.write("trainer.yml")  # Save the model
print(f"{len(np.unique(ids))} faces trained. Exiting program...")
