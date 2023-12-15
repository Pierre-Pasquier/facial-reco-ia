import os
import sys
sys.path.append(os.getcwd())

import cv2
import time
import click
import dlib
import glob
import json
from statistics import mean

from src.evaluation.evaluation import evaluation

@click.command()
@click.option('--face_detector', type=str, help='Path to the face detector model', required=True)
@click.option('--folder_path', type=str, help='Path to the image folder', required=True)
@click.option('--label_path', type=str, help='Path to the label json file', required=False)
@click.option('--iou_threshold', type=float, help='IoU threshold for evaluation', required=False, default=0.5)
@click.option('--resize_factor', type=float, help='Resize image factor', required=False, default=0.5)
@click.option('--use_cpu', is_flag=True, help='Use CPU instead of GPU')
def main(face_detector, folder_path, label_path, iou_threshold, resize_factor, use_cpu):
    if use_cpu:
        detector = dlib.get_frontal_face_detector()
    else:
        detector = dlib.cnn_face_detection_model_v1(face_detector)

    processing_times = []
    true_positives_count, false_positives_count, false_negatives_count = [0, 0, 0]
    
    for f in glob.glob(os.path.join(folder_path, "*.jpg")):
        img = dlib.load_rgb_image(f)

        start = time.time()

        img = cv2.resize(img, (0,0), fx=resize_factor, fy=resize_factor)
        
        dets = detector(img, 1)

        processing_times.append(time.time() - start)

        file_name = f.split("/")[-1]

        print(f"\nFile {file_name}:")
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
        
        if label_path is not None:

            with open(label_path, 'r') as file:
                label_dict = json.load(file)

            detected_boxes = []
            if use_cpu:
                for _, d in enumerate(dets):
                    detected_boxes.append([d.top(), d.right(), d.bottom(), d.left()])
            else:
                for _, d in enumerate(dets):
                    detected_boxes.append([d.rect.top(), d.rect.right(), d.rect.bottom(), d.rect.left()])

            true_positives, false_positives, false_negatives = evaluation(label_dict[file_name], detected_boxes, iou_threshold, resize_factor)
            true_positives_count += true_positives
            false_positives_count += false_positives
            false_negatives_count += false_negatives

    print("\nAverage time taken:", mean(processing_times[1:]))

    if label_path is not None:
        precision = true_positives_count / (true_positives_count + false_positives_count) if (true_positives_count + false_positives_count) > 0 else 0
        recall = true_positives_count / (true_positives_count + false_negatives_count) if (true_positives_count + false_negatives_count) > 0 else 0

        print(f"Global precision: {precision}")
        print(f"Global recall: {recall}")

if __name__ == "__main__":
    main()
