import time
import click
import os
import dlib
import glob
from statistics import mean

@click.command()
@click.option('--shape_predictor', type=str, help='Path to the shape predictor model', required=True)
@click.option('--face_reco', type=str, help='Path to the face recognition model', required=True)
@click.option('--folder_path', type=str, help='Path to the image folder', required=True)
@click.option('--use_cpu', is_flag=True, help='Use CPU instead of GPU')
@click.option('--align', is_flag=True, help='Align the face for better face recognition performances')
def main(shape_predictor, face_reco, folder_path, use_cpu, align):
    if use_cpu:
        # deactivate GPU
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    processing_times_per_face = []
    processing_times_per_image = []
    face_detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(shape_predictor)
    facerec = dlib.face_recognition_model_v1(face_reco)
    
    for f in glob.glob(os.path.join(folder_path, "*.jpg")):
        img = dlib.load_rgb_image(f)

        dets = face_detector(img, 1)

        print(f"\nFile {f}:")
        print("Number of faces detected: {}".format(len(dets)))

        processing_time_img = 0

        # Now process each face we found.
        for k, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))
            
            start = time.time()

            shape = sp(img, d)

            if align:
                face_chip = dlib.get_face_chip(img, shape)
                face_descriptor = facerec.compute_face_descriptor(face_chip)
            else:
                face_descriptor = facerec.compute_face_descriptor(img, shape)

            end = time.time()

            processing_times_per_face.append(end - start)
            processing_time_img += end - start

            print("Face descriptor:", face_descriptor[0])
            print(f"Processing time: {processing_times_per_face[-1]}")
        
        processing_times_per_image.append(processing_time_img)

    print("Average time taken per face:", mean(processing_times_per_face[1:]))
    print("Average time taken per image:", mean(processing_times_per_image[1:]))

if __name__ == "__main__":
    main()
