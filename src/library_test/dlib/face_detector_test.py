import time
import click
import os
import dlib
import glob
from statistics import mean

@click.command()
@click.option('--face_detector', type=str, help='Path to the face detector model', required=True)
@click.option('--folder_path', type=str, help='Path to the image folder', required=True)
@click.option('--use_cpu', is_flag=True, help='Use CPU instead of GPU')
def main(face_detector, folder_path, use_cpu):
    if use_cpu:
        detector = dlib.get_frontal_face_detector()
    else:
        detector = dlib.cnn_face_detection_model_v1(face_detector)

    processing_times = []
    
    for f in glob.glob(os.path.join(folder_path, "*.jpg")):
        img = dlib.load_rgb_image(f)
        start = time.time()
        dets = detector(img, 1)
        processing_times.append(time.time() - start)
        print(f"\nFile {f}:")
        print("Number of faces detected: {}".format(len(dets)))
        print(f"Processing time: {processing_times[-1]}")

        if use_cpu:
            for k, d in enumerate(dets):
                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    k, d.left(), d.top(), d.right(), d.bottom()))

        else:
            for i, d in enumerate(dets):
                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
                    i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

    print("Average time taken:", mean(processing_times[1:]))

if __name__ == "__main__":
    main()
