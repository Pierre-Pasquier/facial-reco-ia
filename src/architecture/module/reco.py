import os
import cv2
import dlib
import glob


shape_predictor = 'models/shape_predictor_5_face_landmarks.dat'
face_reco = 'models/dlib_face_recognition_resnet_model_v1.dat'
folder_path = 'src/architecture/images/temp'

sp = dlib.shape_predictor(shape_predictor)
facerec = dlib.face_recognition_model_v1(face_reco)

for f in glob.glob(os.path.join(folder_path, "*.jpg")):
    img = dlib.load_rgb_image(f)

    height, width = img.shape[0], img.shape[1]

    rect = dlib.rectangle(left=0, top=0, right=width, bottom=height)

    shape = sp(img, rect)

    face_chip = dlib.get_face_chip(img, shape)
    face_descriptor = facerec.compute_face_descriptor(face_chip)
