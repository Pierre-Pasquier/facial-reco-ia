import time
import click
import os
from deepface import DeepFace

backends = [
    'opencv',
    'ssd',
    'mtcnn',
    'retinaface'
]

@click.command()
@click.option('--img_path', type=str, help='Path to the image file', required=True)
@click.option('--use_cpu', is_flag=True, help='Use CPU instead of GPU')
def main(img_path, use_cpu):
    if use_cpu:
        # deactivate GPU
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # for initialization
    DeepFace.represent(img_path=img_path, detector_backend='opencv')

    for backend in backends:
        print(f"\nUsing backend: {backend}")
        start = time.time()

        try:
            embedding_objs = DeepFace.represent(img_path=img_path, detector_backend=backend)
            print(f"Time taken: {time.time() - start} seconds")

            for i, obj in enumerate(embedding_objs):
                print(f"Facial Area {i + 1}: {obj['facial_area']}")
        except Exception as e:
            print(f"Error with backend {backend}: {e}")

if __name__ == "__main__":
    main()
