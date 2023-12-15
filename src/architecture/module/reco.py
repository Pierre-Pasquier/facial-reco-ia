import os
import dlib
import glob
import numpy as np


shape_predictor = 'models/shape_predictor_5_face_landmarks.dat'
face_reco = 'models/dlib_face_recognition_resnet_model_v1.dat'
folder_path = 'src/architecture/images'

sp = dlib.shape_predictor(shape_predictor)
facerec = dlib.face_recognition_model_v1(face_reco)

person_vectors = []

for f in glob.glob(os.path.join(folder_path, 'persons', "*", "*.txt")):
    with open(f, 'r') as file:
        person_vectors += [
            np.array(eval(file.readline()))
        ]

for f in glob.glob(os.path.join(folder_path, 'temp', "*.jpg")):
    img = dlib.load_rgb_image(f)

    height, width = img.shape[0], img.shape[1]

    rect = dlib.rectangle(left=0, top=0, right=width, bottom=height)

    shape = sp(img, rect)

    face_chip = dlib.get_face_chip(img, shape)
    face_descriptor = facerec.compute_face_descriptor(face_chip)

    for i in range(len(person_vectors)):
        distance = np.linalg.norm(person_vectors[i] - np.array(face_descriptor))

        if distance > 0.43:
            # TODO
            # register in new directory
            # calculate representing vector
            exit()
        else:
            # TODO
            # register in existing directory
            # update representing vector
            exit()
