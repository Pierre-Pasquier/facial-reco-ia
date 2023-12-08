# Test of DeepFace library

## Face detectors test

To test each available face detectors model (OpenCV, SSD, MTCNN, RetinaFace), use the following command:

```bash
python3 face_detectors_test.py --img_path <path_to_img>
```

This script take an optionnal command `--use_cpu` if you want to use CPU instead of GPU (default).

## Add legend to video

To add a legend to a video using OpenCV. Should not be used anymore because this code was added to the labeling files.

*Need to be run at the root of the project*

## Deepface Labeling videos

To label several videos with several models. Videos and models can be chosen inside the file. Each video produced is only labeled by one model at a time

 *Need to be run at the root of the project*

## Deepface multi model labeling

To label a single video with every deepface detection model at the same time. Each model is represented by a color, the legend is written at the top of the video and the mean labeling time by frames for each model is written at the bottom right of the video

 *Need to be run at the root of the project*

## Test deepface

Contains some functions to test deepface :

- face_recognition(image_path) : apply face recognition on the given image 
- analyze_face(image_path) : analyze the person on the given image and return age, gender, race and emotion of htis person
- get_embeddings(image_path) : Find where is the person on the given image
- camera_analyze_test() : apply the analyze function on each frame of the webcam video live stream
- camera_detection_test() : apply the detection function on each frame of the webcam video live stream




