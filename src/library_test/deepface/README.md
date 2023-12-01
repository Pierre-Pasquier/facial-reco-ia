# Test of DeepFace library

## Face detectors test

To test each available face detectors model (OpenCV, SSD, MTCNN, RetinaFace), use the following command:

```bash
python3 face_detectors_test.py --img_path <path_to_img>
```

This script take an optionnal command `--use_cpu` if you want to use CPU instead of GPU (default).