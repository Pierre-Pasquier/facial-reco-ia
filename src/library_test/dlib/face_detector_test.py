import time
import click
import os
import dlib
import glob
from statistics import mean

@click.command()
@click.option('--folder_path', type=str, help='Path to the image folder', required=True)
@click.option('--use_cpu', is_flag=True, help='Use CPU instead of GPU')
def main(folder_path, use_cpu):
    if use_cpu:
        # deactivate GPU
        os.environ["CUDA_VISIBLE_DEVICES"] = ""

    processing_times = []
    detector = dlib.get_frontal_face_detector()
    
    for f in glob.glob(os.path.join(folder_path, "*.jpg")):
        img = dlib.load_rgb_image(f)
        start = time.time()
        dets = detector(img, 1)
        processing_times.append(time.time() - start)
        print(f"\nFile {f}:")
        print("Number of faces detected: {}".format(len(dets)))
        print(f"Processing time: {processing_times[-1]}")

        # Now process each face we found.
        for k, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))

    print("Average time taken:", mean(processing_times))

if __name__ == "__main__":
    main()
