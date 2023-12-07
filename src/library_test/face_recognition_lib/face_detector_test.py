import time
import click
import os
import glob
import face_recognition
from statistics import mean

@click.command()
@click.option('--folder_path', type=str, help='Path to the image folder', required=True)
def main(folder_path):
    processing_times = []
    
    for f in glob.glob(os.path.join(folder_path, "*.jpg")):
        image = face_recognition.load_image_file(f)
        start = time.time()
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        processing_times.append(time.time() - start)
        print(f"\nFile {f}:")
        print("Number of faces detected: {}".format(len(face_locations)))
        print(f"Processing time: {processing_times[-1]}")

        for k, face_location in enumerate(face_locations):

            top, right, bottom, left = face_location
            print(f"Detection {k}: Left: {left} Top: {top} Right: {right} Bottom: {bottom}")

    print("Average time taken:", mean(processing_times[1:]))

if __name__ == "__main__":
    main()
