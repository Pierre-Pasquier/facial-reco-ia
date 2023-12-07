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

This script is interesting to evaluate visually the precision of the face detection model.

### Face detection test

The script `face_detector_test.py` evaluate the time taken by the face detector to evaluate the positions of faces.

You can launch it with the following command:
```bash
python3 face_recognition.py --folder_path <image_folder_path>
```

### Face recognition test

The script `face_reco_test.py` evaluate the time taken by the face recognition model to calculate the vector identifying a face.

You can launch it with the following command:
```bash
python3 face_reco_test.py \
    --shape_predictor <shape_predictor_model_path> \
    --face_reco <face_recognition_model_path> \
    --folder_path <image_folder_path>
```

This script take optionnal commands:
- `--use_cpu` if you want to use CPU instead of GPU (default);
- `--align` if you want to align the face for better face recognition performances.
