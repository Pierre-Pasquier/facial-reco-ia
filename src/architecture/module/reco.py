import os
import sys
import dlib
import glob
import click
import time
import numpy as np


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Activate the verbose', required=False)
@click.option('--threshold', '-t', type=float, help='Recognition threshold', required=False, default=0.43)
def main(verbose, threshold):
    shape_predictor = 'models/shape_predictor_5_face_landmarks.dat'
    face_reco = 'models/dlib_face_recognition_resnet_model_v1.dat'
    folder_path = 'images'

    start_load_model = time.time()

    sp = dlib.shape_predictor(shape_predictor)
    facerec = dlib.face_recognition_model_v1(face_reco)

    if verbose:
        print(f"TIME TO LOAD MODELS: {time.time() - start_load_model}")

    person_vectors = {}
    new_persons_detected = 0
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
        min_distance = float('inf')
        
        # get the best corresponding known person
        for key, data in distance_summary.items():
            distance = data['distance']
            if distance < min_distance:
                min_key = key
                min_distance = distance

        if min_distance >= threshold:
            # register in new directory
            new_directory = os.path.join(folder_path, 'persons', str(person_idx))
            os.makedirs(new_directory)
            person_idx += 1
            # initialize representing vector, by launching a new processe
            with open(os.path.join(new_directory, 'descriptor.txt'), 'w') as file:
                file.write(str(list(face_descriptor)))
                file.flush()
                # os.system(f"echo \"{list(face_descriptor)}\" > {new_directory}/descriptor.txt ")
            os.rename(f, os.path.join(new_directory, os.path.basename(f)))
            # update known person dict
            person_vectors[new_directory] = np.array(face_descriptor)
            # update new persons registered count
            new_persons_detected += 1

        if min_distance < threshold:
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
                # os.system(f"echo \"{list(new_vector)}\" > {min_key}/descriptor.txt ")
            # update known person dict
            person_vectors[min_key] = new_vector

    if verbose:
        print(f"NEW PERSONS DETECTED: {new_persons_detected}")
    
    print("1", file=sys.stderr)

if __name__ == "__main__":    
    main()
