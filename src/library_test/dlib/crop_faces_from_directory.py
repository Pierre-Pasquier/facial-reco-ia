import dlib
import cv2
import glob
import os
import click

@click.command()
@click.option('--entry_folder', type=str, help='Path to the entry image folder', required=True)
@click.option('--exit_folder', type=str, help='Path to the exit image folder', required=True)
def main(entry_folder, exit_folder):
    detector = dlib.get_frontal_face_detector()
    
    def save_cropped_faces(faces, image, file):
        # Save cropped faces as separate images in a directory
        for i, face in enumerate(faces):
            print(face)
            (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
            cropped_face = image[y:y+h, x:x+w]
            os.makedirs(exit_folder, exist_ok=True)
            cv2.imwrite(os.path.join(exit_folder, os.path.basename(file)), cropped_face)

    ### IMAGE PROCESSING LOOP ###
    for f in glob.glob(os.path.join(entry_folder, "*.jpg")):
        img = dlib.load_rgb_image(f)

        dets = detector(img, 1)

        if dets != []:
            save_cropped_faces(dets, img, f)

if __name__ == "__main__":
    main()