import cv2
import numpy as np

from utils.imgTransform import cartoon_effect, edge_detect, face_detect, face_detect_cvlib, gender_recog_cvlib, object_detect_cvlib


def processPhoto(image, transform):
    img_np = np.frombuffer(image, dtype=np.ubyte)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if transform == "object":
        img = object_detect_cvlib(img)

    elif transform == "face":
        img = face_detect(img)

    elif transform == "facecv":
        img = face_detect_cvlib(img)

    elif transform == "gender":
        img = gender_recog_cvlib(img)

    elif transform == "edges":
        img = edge_detect(img)

    elif transform == "cartoon":
        img = cartoon_effect(img)

    image_bytes = cv2.imencode('.png', img)[1]

    return image_bytes
