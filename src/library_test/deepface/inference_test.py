import time
from deepface import DeepFace

backends = [
    'opencv',
    'ssd',
    'dlib',
    'mtcnn',
    'retinaface',
    'mediapipe',
    'yolov8',
    'yunet',
    'fastmtcnn',
]

img_path = "data/face_small_dataset/dataset/9_Press_Conference_Press_Conference_9_45.jpg"

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
