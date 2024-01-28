import os
import sys
import dlib
import glob
import click
import time
import shutil
import random as rd
import numpy as np


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Activate the verbose', required=False)
@click.option('--random', '-r', is_flag=True, help='Activate random image selection', required=False)
@click.option('--threshold', '-t', type=float, help='Recognition threshold', required=False, default=0.43)
def main(verbose, random, threshold):
    # models path
    shape_predictor = 'models/shape_predictor_5_face_landmarks.dat'
    face_reco = 'models/dlib_face_recognition_resnet_model_v1.dat'
    folder_path = 'images'

    # list of all faces in temp directory
    new_faces_list = [f for f in glob.glob(os.path.join(folder_path, 'temp', "*.jpg"))]

    # shuffle the list if necessary
    if random:
        rd.shuffle(new_faces_list)
    
    if verbose:
        ### LOAD MODEL TIME TEST ###
        start_load_model = time.time()

        sp = dlib.shape_predictor(shape_predictor)
        facerec = dlib.face_recognition_model_v1(face_reco)
        # inference test
        if new_faces_list != []:
            calculate_face_descriptor(sp, facerec, new_faces_list[0])

        print(f"TIME TO LOAD MODELS: {time.time() - start_load_model}")
        ############################
    else:
        sp = dlib.shape_predictor(shape_predictor)
        facerec = dlib.face_recognition_model_v1(face_reco)

    person_vectors = {}
    new_persons_detected_count = 0
    person_idx = len(os.listdir(os.path.join(folder_path, 'persons')))

    # get the descriptor of all persons in persons directory
    for f in glob.glob(os.path.join(folder_path, 'persons', "*", "descriptor.txt")):
        # if the descriptor is empty, open the backup file
        with open(f, 'r') as file:
            descriptor_content = file.readline().strip()

            # if descriptor empty
            if not descriptor_content:
                if verbose:
                    print(f"DESCRIPTOR EMPTY, BACKUP FILE USED FOR FILE: {f}")
                backup_file_path = os.path.join(os.path.dirname(f), "backup_descriptor.txt")
                with open(backup_file_path, 'r') as file:
                    directory = os.path.dirname(f)
                    person_vectors[directory] = np.array(eval(file.readline()))
                # replace descriptor by backup file
                shutil.copy(os.path.join(os.path.dirname(f), "backup_descriptor.txt"), os.path.join(os.path.dirname(f), "descriptor.txt"))

            # if descriptor file not empty
            else:
                with open(f, 'r') as file:
                    directory = os.path.dirname(f)
                    person_vectors[directory] = np.array(eval(descriptor_content))

    # iterate on new faces in temp file
    for f in new_faces_list:
        face_descriptor = calculate_face_descriptor(sp, facerec, f)

        distance_summary = {}
        
        # iterate on all persons in persons directory to calculate distance
        for key, value in person_vectors.items():
            distance = np.linalg.norm(value - np.array(face_descriptor))

            distance_summary[key] = {'value': value, 'distance': distance}
        
        min_key = None
        min_distance = float('inf')
        
        # get the smallest distance between new face and all persons faces
        for key, data in distance_summary.items():
            distance = data['distance']
            if distance < min_distance:
                min_key = key
                min_distance = distance

        # distance is here too long, so it is a new person
        if min_distance >= threshold:
            register_new_person(folder_path, person_idx, face_descriptor, person_vectors, f)
            person_idx += 1
            new_persons_detected_count += 1

        # distance is here small, so it is a already registered person
        if min_distance < threshold:
            register_known_person(min_key, face_descriptor, person_vectors, f)

    if verbose:
        print(f"NEW PERSONS DETECTED: {new_persons_detected_count}")
    
    print("1", file=sys.stderr)


def calculate_face_descriptor(shape_predictor, face_recognition, image_file):
    """Assign a 128D vector to a face image, identifying an unique person.

    Args:
        shape_predictor: shape predictor model.
        face_recognition: face recognition model.
        image_file (str): path of the image file.

    Returns:
        face_descriptor: 128D vector identifying an unique person.
    """
    img = dlib.load_rgb_image(image_file)

    height, width = img.shape[0], img.shape[1]

    rect = dlib.rectangle(left=0, top=0, right=width, bottom=height)

    shape = shape_predictor(img, rect)

    face_chip = dlib.get_face_chip(img, shape)
    face_descriptor = face_recognition.compute_face_descriptor(face_chip)

    return face_descriptor

def register_new_person(folder_path, person_idx, face_descriptor, person_vectors, f) -> None:
    """Register a person in a new directory.

    Args:
        folder_path (str): path of the folder.
        person_idx (int): id representing the total of known persons.
        face_descriptor: 128D vector identifying an unique person.
        person_vectors (dict): dictionnary of descriptors of all persons in persons directory
        f: new face path file
    """
    # register in new directory
    new_directory = os.path.join(folder_path, 'persons', str(person_idx))
    os.makedirs(new_directory)
    
    # initialize representing vector
    with open(os.path.join(new_directory, 'descriptor.txt'), 'w') as file:
        file.write(str(list(face_descriptor)))
        file.flush()

    # make a backup
    shutil.copy(os.path.join(new_directory, 'descriptor.txt'), os.path.join(new_directory, 'backup_descriptor.txt'))
    
    # move file
    os.rename(f, os.path.join(new_directory, os.path.basename(f)))

    # update known person dict
    person_vectors[new_directory] = np.array(face_descriptor)

def register_known_person(min_key, face_descriptor, person_vectors, f):
    # register in existing directory
    os.rename(f, os.path.join(min_key, os.path.basename(f)))

    # update representing vector
    old_vector = None
    nb_img = len(os.listdir(min_key)) - 1
    with open(os.path.join(min_key, 'descriptor.txt'), 'r') as file:
        old_vector = np.array(eval(file.readline()))
    new_vector = (old_vector * nb_img + np.array(face_descriptor)) / (nb_img + 1)

    # update the descriptor file
    with open(os.path.join(min_key, 'descriptor.txt'), 'w') as file:
        file.write(str(list(new_vector)))
        file.flush()

    # update backup file by overwriting it with descriptor copy
    shutil.copy(os.path.join(min_key, 'descriptor.txt'), os.path.join(min_key, 'backup_descriptor.txt'))

    # update known person dict
    person_vectors[min_key] = new_vector


if __name__ == "__main__":    
    main()
