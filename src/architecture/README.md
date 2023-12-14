# Architecture

This folder contains all the necessary files for a functional recognition pipeline. For a better understanding, please look a the following schema: `schemas/architecture.png`.

## Images

This folder contains face images and associated vectors.

### Temp

Temporary folder where the `module/faces.py` script will register the detected faces.

### Persons

Database folder where the `module/reco.py` script will register new persons detected, or add faces to already existing persons.

## Module

Folder containing all the python scripts for a functional pipeline.

### Faces

This script role is to:
- Launch a new GStreamer pipeline.
- Run while no faces are detected.
- When a face is detected, exit the script and register in the `images/temp` folder all the croped faces detected.

### Reco

This script role is to:
- Calculate all the vectors of the faces in the `images/temp` folder.
- Register the faces

## Schemas

This folder contains the schemas designing the architecture.
