#!/bin/bash

mkdir -p models
cd models

curl -LJO http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2
curl -LJO http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
curl -LJO http://dlib.net/files/mmod_human_face_detector.dat.bz2

bzip2 -d shape_predictor_5_face_landmarks.dat.bz2
bzip2 -d dlib_face_recognition_resnet_model_v1.dat.bz2
bzip2 -d mmod_human_face_detector.dat.bz2

echo "Models downloaded and extracted successfully."