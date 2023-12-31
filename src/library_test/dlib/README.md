# DLib Library

## Download models

Go to the project root and do the following commands to download the two required models:
```bash
chmod 777 bash/dlib_models.sh
./bash/dlib_models.sh
```

## Face detection and recognition script

The script `official_examples/detection_and_recognition.py` was download at the following [link](http://dlib.net/face_recognition.py.html).

You can launch it with the following command:
```bash
python3 detection_and_recognition.py <shape_predictor_model_path> <face_recognition_model_path> <image_folder_path>
```

This script is interesting to evaluate visually the precision of the face detection model.

### Face detection test

The script `face_detector_test.py` evaluate the time taken by the face detector to evaluate the positions of faces.

You can launch it with the following command:
```bash
python3 face_detector_test.py \
    --face_detector <face_detector_model_path> \
    --folder_path <image_folder_path>
```

This script take optionnal commands:
- `--label_path <label_file_path>` if you want to do an evaluation of the detector;
- `--iou_threshold <float_min_iou>` to specify the threshold you want to use to consider one detection correct;
- `--resize_factor <float_resize_factor>` to specify the resize factor of the image;
- `--use_cpu` if you want to use CPU instead of GPU (default).

Here are the results of the script running with the jetson nano orin (GPU) on the small dataset:
- Average time taken per image: 0.29 seconds

### Face recognition test

The script `face_reco_test.py` evaluate the time taken by the face recognition model to calculate the vector identifying a face.

You can launch it with the following command:
```bash
python3 face_reco_test.py \
    --face_detector <face_detector_model_path> \
    --shape_predictor <shape_predictor_model_path> \
    --face_reco <face_recognition_model_path> \
    --folder_path <image_folder_path>
```

This script take optionnal commands:
- `--align` if you want to align the face for better face recognition performances.

Here are the results of the script running with the jetson nano orin (GPU) on the small dataset:
- Average time taken per face: 0.012 seconds
- Average time taken per image: 0.036 seconds
