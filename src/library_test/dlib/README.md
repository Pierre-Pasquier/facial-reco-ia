# DLib Library

## Dowload models

Go to the project root and do the following commands to download the two required models:
```bash
chmod 777 bash/dlib_models.sh
./bash/dlib_models.sh
```

## Face detection and recognition script

The script `detection_and_recognition.py` was download at the following [link](http://dlib.net/face_recognition.py.html).

You can launch it with the following command:
```bash
python3 face_recognition.py <shape_predictor_model_path> <face_recognition_model_path> <image_folder_path>
```