import os
import sys
sys.path.append(os.getcwd())

import time
import click
import glob
import face_recognition
import json
from statistics import mean

from src.evaluation.evaluation import evaluation


@click.command()
@click.option('--folder_path', type=str, help='Path to the image folder', required=True)
@click.option('--label_path', type=str, help='Path to the label json file', required=False)
@click.option('--iou_threshold', type=float, help='IoU threshold for evaluation', required=False, default=0.5)
def main(folder_path, label_path, iou_threshold):
    processing_times = []
    
    for f in glob.glob(os.path.join(folder_path, "*.jpg")):
        image = face_recognition.load_image_file(f)

        start = time.time()

        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0) #, model="cnn")

        processing_times.append(time.time() - start)

        file_name = f.split("/")[-1]

        print(f"\nFile {file_name}:")
        print("Number of faces detected: {}".format(len(face_locations)))
        print(f"Processing time: {processing_times[-1]}")

        for k, face_location in enumerate(face_locations):

            top, right, bottom, left = face_location
            print(f"Detection {k}: Left: {left} Top: {top} Right: {right} Bottom: {bottom}")

        if label_path is not None:

            with open(label_path, 'r') as file:
                label_dict = json.load(file)

            evaluation(label_dict[file_name], face_locations, iou_threshold)

    print("Average time taken:", mean(processing_times[1:]))

if __name__ == "__main__":
    main()
