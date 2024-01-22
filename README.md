# facial-reco-ia

Main repository of the project with all the codes used relating to AI and facial recognition respecting a classical folder structure (source, tests, models...)

## Installation

After completing the [following tutorial](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#next), we can notice that JetPack is already installed using this command:
```bash
sudo apt-cache show nvidia-jetpack
```

### Tensorflow

Tensorflow is required for Deepface and DLib libraries.

Check [this link](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html) to install the JetPack compatible version of TensorFlow:

For GPU monitoring:
```bash
sudo pip3 install -U jetson-stats
jtop
```

### PyTorch, TorchVision

First, install ultralitycs following the tutorial in the section below, because if you install it after it will replace the PyTorch version.

#### PyTorch

PyTorch is necessary for runnning the yolov8 with the Ultralytics library. Check [this link](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#overview) to install the JetPack compatible version of PyTorch.

If you are facing any problems, you can also install everything from the wheel from [here](https://developer.download.nvidia.com/compute/redist/jp/v512/).

#### TorchVision

You now have to install a compatible version of TorchVision with PyTorch. You can find the compatible matrix [here](https://github.com/pytorch/vision#installation).

Do not install TorchVision with pip, but from source like explained [here](https://forums.developer.nvidia.com/t/pytorch-compatibility-issues-torch-2-0-0-nv23-5-torchvision-0-15-1/256116).

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

### Ultralytics

This library is necessary to use easily yolov8 for person recognition.
```bash
pip install ultralytics
```

If you already installed PyTorch and TorchVision, please do this and then install necessary dependancies following [this link](https://github.com/ultralytics/ultralytics/blob/main/pyproject.toml).
```bash
pip install ultralytics --no-deps
```

## Troubleshooting

**Trouble**:
Running the script `src/library_test/dlib/face_detector_test.py`, the Jetson Nano Orin devkit was crashing because of RAM excessive use.

**Solution**: 
Use images with smaller resolution prevent the crash of the devkit.
