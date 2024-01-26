import dlib
import cv2
import glob
import os
import shutil
import random
from tqdm import tqdm


def save_cropped_faces(faces, image, file, exit_folder):
    # save cropped faces as separate images in a directory
    for i, face in enumerate(faces):
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        cropped_face = image[y:y+h, x:x+w]
        if x >= 0 and y >= 0 and w >= 0 and h >= 0:
            os.makedirs(exit_folder, exist_ok=True)
            cv2.imwrite(os.path.join(exit_folder, os.path.basename(file)), cropped_face)

def crop_directory(entry_folder, exit_folder):
    detector = dlib.get_frontal_face_detector()

    ### IMAGE PROCESSING LOOP ###
    for f in glob.glob(os.path.join(entry_folder, "*.jpg")):
        img = dlib.load_rgb_image(f)

        dets = detector(img, 1)

        if dets != []:
            save_cropped_faces(dets, img, f, exit_folder)

def crop_dataset(dataset_folder, new_dataset_path, nb_folder):
    all_directories = [d for d in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, d))]

    for _ in tqdm(range(nb_folder), desc="Processing cropping"):
        random_directory = random.choice(all_directories)

        crop_directory(os.path.join(dataset_folder, random_directory), os.path.join(new_dataset_path, random_directory + "_cropped"))

        all_directories.remove(random_directory)

def copy_all_images(dataset_path):
    os.makedirs(os.path.join(dataset_path, "_all"), exist_ok=True)

    all_directories = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

    for dir in tqdm(all_directories, desc="Proccessing copy of all images"):
        if dir != "_all":
            for f in os.listdir(os.path.join(dataset_path, dir)):
                shutil.copy(os.path.join(dataset_path, dir, f), os.path.join(dataset_path, "_all", f))


def main(dataset_folder, new_dataset_path, nb_folder):
    crop_dataset(dataset_folder, new_dataset_path, nb_folder)
    copy_all_images(new_dataset_path)


if __name__ == "__main__":
    dataset_folder = "data/lfw"
    new_dataset_path = "data/lfw_cropped"
    subdirectories = [d for d in os.listdir(dataset_folder) if os.path.isdir(os.path.join(dataset_folder, d))]
    nb_folder = len(subdirectories)

    main(dataset_folder, new_dataset_path, nb_folder)