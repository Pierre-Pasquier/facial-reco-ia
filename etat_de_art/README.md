# State of the Art

## Datasets

### Images

#### Face detection

[Face Detection in Images](https://www.kaggle.com/datasets/dataturks/face-detection-in-images): 500 images, 1.1k faces

#### Face recognition

##### Training

[VGG2](https://drive.google.com/file/d/1dyVQ7X3d28eAcjV3s3o0MT-HyODp_v3R/view?usp=sharing): 3.31m images, 9k people

[WebFace260million](https://www.face-benchmark.org/download.html): 260m images, 4m people

##### Benchmark

[LFW: Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/): 13k images, 5k people

### Videos

#### Face recognition

[YTF: YouTube Faces](https://www.cs.tau.ac.il/~wolf/ytfaces/): 3.4k videos, 1.5k people

## Person Detection

### YOLO

https://github.com/AlexeyAB/darknet

YOLO is a text configuration file defining how neural networks are built and behave. YOLOv4 is the most recent version of YOLO. YOLOv4-tiny is a smaller/faster version of YOLOv4. It is possible to train a YOLO model to detect custom objects, using the pre-trained weights-files.

Here are the model structure of [YOLOv4](https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg) and [YOLOv4-tiny](https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg).

Here are the model weights of [YOLOv4](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights) and [YOLOv4-tiny](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights).

## Face Detection

[HOG (DLib, DeepFace)](http://dlib.net/face_detector.py.html)

[Haar-Cascade (Open-CV, DeepFace)](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)

[MTCNN: Multi-Task Cascaded Convolutional Neural Network (DeepFace)](https://github.com/ipazc/mtcnn)

[SSD: Single-Shot multiBox Detector (DeepFace)](https://arxiv.org/abs/1512.02325)

## Face Recognition

### Models

[VGG-Face](https://www.robots.ox.ac.uk/~vgg/software/vgg_face)
LFW: 99.78%
YTF: 97.40%

[Google FaceNet](https://arxiv.org/abs/1503.03832)
LFW: 99.20%

[OpenFace](https://cmusatyalab.github.io/openface/)
LFW: 93.80%

[DeepID](https://arxiv.org/pdf/2001.07871.pdf)
YTF: 97.05%

[Dlib](http://dlib.net/face_recognition.py.html)
LFW: 99.38%

[ArcFace](https://insightface.ai/arcface)
LFW: 99.41%

### Librairies

[Face Recognition](https://github.com/ageitgey/face_recognition)

[DeepFace](https://github.com/serengil/deepface)
