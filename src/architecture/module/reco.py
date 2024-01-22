import os
import sys
import dlib
import glob
import numpy as np


shape_predictor = 'models/shape_predictor_5_face_landmarks.dat'
face_reco = 'models/dlib_face_recognition_resnet_model_v1.dat'
folder_path = 'images'

sp = dlib.shape_predictor(shape_predictor)
facerec = dlib.face_recognition_model_v1(face_reco)

person_vectors = {}
person_idx = len(os.listdir(os.path.join(folder_path, 'persons')))

# get the descriptor of all known persons
for f in glob.glob(os.path.join(folder_path, 'persons', "*", "*.txt")):
    with open(f, 'r') as file:
        directory = os.path.dirname(f)
        person_vectors[directory] = np.array(eval(file.readline()))

# iterate on new faces
for f in glob.glob(os.path.join(folder_path, 'temp', "*.jpg")):
    img = dlib.load_rgb_image(f)

    height, width = img.shape[0], img.shape[1]

    rect = dlib.rectangle(left=0, top=0, right=width, bottom=height)

    shape = sp(img, rect)

    face_chip = dlib.get_face_chip(img, shape)
    face_descriptor = facerec.compute_face_descriptor(face_chip)

    distance_summary = {}
    
    # iterate on each known persons to calculate distance
    for key, value in person_vectors.items():
        distance = np.linalg.norm(value - np.array(face_descriptor))

        distance_summary[key] = {'value': value, 'distance': distance}
    
    min_key = None
    min_value = None
    min_distance = float('inf')
    
    # get the best corresponding known person
    for key, data in distance_summary.items():
        distance = data['distance']
        if distance < min_distance:
            min_key = key
            min_value = data['value']
            min_distance = distance

    if min_distance >= 0.40:
        # register in new directory
        new_directory = os.path.join(folder_path, 'persons', str(person_idx))
        os.makedirs(new_directory)
        os.rename(f, os.path.join(new_directory, os.path.basename(f)))
        person_idx += 1
        # initialize representing vector
        with open(os.path.join(new_directory, 'descriptor.txt'), 'w') as file:
            file.write(str(list(face_descriptor)))
        # update known person dict
        person_vectors[new_directory] = np.array(face_descriptor)

    if min_distance < 0.40:
        # register in existing directory
        os.rename(f, os.path.join(min_key, os.path.basename(f)))
        # update representing vector
        old_vector = None
        nb_img = len(os.listdir(min_key)) - 1
        with open(os.path.join(min_key, 'descriptor.txt'), 'r') as file:
            old_vector = np.array(eval(file.readline()))
        new_vector = (old_vector * nb_img + np.array(face_descriptor)) / (nb_img + 1)
        with open(os.path.join(min_key, 'descriptor.txt'), 'w') as file:
            file.write(str(list(new_vector)))
        # update known person dict
        person_vectors[min_key] = new_vector

print("1", file=sys.stderr)
