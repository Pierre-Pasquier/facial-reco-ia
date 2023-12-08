# Face Recognition Library

## Face detection test

The script `face_detector_test.py` evaluate the time taken by the face detector to evaluate the positions of faces. It was inspired by the [following script](https://github.com/ageitgey/face_recognition/blob/master/examples/find_faces_in_picture_cnn.py).

You can launch it with the following command:
```bash
python3 src/library_test/dlib/face_detector_test.py \
    --folder_path <image_folder_path>
```

This script take optionnal commands:
- `--label_path <label_file_path>` if you want to do an evaluation of the detector;
- `--iou_threshold <float_min_iou>` to specify the threshold you want to use to consider one detection correct;
- `--use_cpu` if you want to use CPU instead of GPU (default).
