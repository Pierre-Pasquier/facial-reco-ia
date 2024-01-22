import dlib
import cv2
import glob
import os
import random


def save_cropped_faces(faces, image, file, exit_folder):
    # save cropped faces as separate images in a directory
    for i, face in enumerate(faces):
        print(face)
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        cropped_face = image[y:y+h, x:x+w]
        os.makedirs(exit_folder, exist_ok=True)
        cv2.imwrite(os.path.join(exit_folder, os.path.basename(file)), cropped_face)

def crop_directory(entry_folder, exit_folder):
    detector = dlib.get_frontal_face_detector()

    # TODO
    print(entry_folder, exit_folder)

    ### IMAGE PROCESSING LOOP ###
    for f in glob.glob(os.path.join(entry_folder, "*.jpg")):
        img = dlib.load_rgb_image(f)

        dets = detector(img, 1)

        if dets != []:
            save_cropped_faces(dets, img, f, exit_folder)

def crop_dataset(dataset_folder, new_dataset_path, nb_folder):
    all_directories = [d for d in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, d))]

    for _ in range(nb_folder):
        random_directory = random.choice(all_directories)

        # TODO
        print(random_directory)

        crop_directory(os.path.join(dataset_folder, random_directory), os.path.join(new_dataset_path, random_directory + "_cropped"))

        all_directories.remove(random_directory)

def main(dataset_folder, new_dataset_path, nb_folder):
    crop_dataset(dataset_folder, new_dataset_path, nb_folder)


if __name__ == "__main__":
    dataset_folder = "data/lfw"
    new_dataset_path = "data/lfw_cropped"
    nb_folder = 10

    main(dataset_folder, new_dataset_path, nb_folder)