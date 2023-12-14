# facial-reco-ia

Main repository of the project with all the codes used relating to AI and facial recognition respecting a classical folder structure (source, tests, models...)

## Installation

After completing the [following tutorial](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#next), we can notice that JetPack is already installed using this command:
```bash
sudo apt-cache show nvidia-jetpack
```

Check this link to install the JetPack compatible version of TensorFlow:
https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

For GPU monitoring:
```bash
sudo pip3 install -U jetson-stats
jtop
```

### DeepFace

To install deepface without changing the compatible version of tensorflow, run the following command:
```bash
pip install deepface --no-deps
pip install tqdm
pip install fire
pip install Flask
pip install gdown
pip install gunicorn
pip install mtcnn
pip install opencv-python
pip install retina-face
```

### DLib

You can directly use the following command to install dlib:
```bash
pip install dlib
```

To download the models using the bash script `bash/dlib_models.sh`, don't forget to have `curl` installed:
```bash
sudo apt install curl
```

## Troubleshooting

**Trouble**:
Running the script `src/library_test/dlib/face_detector_test.py`, the Jetson Nano Orin devkit was crashing because of RAM excessive use.

**Solution**: 
Use images with smaller resolution prevent the crash of the devkit.
