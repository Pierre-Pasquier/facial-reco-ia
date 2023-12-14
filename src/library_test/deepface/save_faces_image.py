from deepface import DeepFace
import cv2
import numpy as np
import sys, time, math
from  collections import deque
import time
import os



directory = os.getcwd() + '/data/videos_test/'



video_name = 'Crowd walking on street cropped.mp4'





video = cv2.VideoCapture(directory + video_name)

# Initialize some variables
face_locations = []

length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(video.get(3)) 
frame_height = int(video.get(4))
size = (frame_width, frame_height)

ret = True
current_frame = 0




while ret :
    current_frame += 1
    print("Currently at frame " + str(current_frame) + " out of " + str(length))
    # Grab a single frame of video
    ret, frame = video.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    try :
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    except :
        ret, frame = video.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    # Find all the faces and face encodings in the current frame of video
    try :
        face_locations = DeepFace.represent(frame, detector_backend = 'opencv')
    except :
        face_locations = []



    if len(face_locations) != 0:
        for k in range(len(face_locations)):
            x, y, w, h = face_locations[k]['facial_area']['x'], face_locations[k]['facial_area']['y'], face_locations[k]['facial_area']['w'], face_locations[k]['facial_area']['h']
            
            # Save the image of the detected face
            face_image = frame[y:y+h, x:x+w]
            save_path = os.getcwd() + '/src/architecture/save_faces/faces_saved/face_' + str(k) + '_frame_' + str(current_frame) + '.jpg'
            cv2.imwrite(save_path, face_image)
            print("Face saved at:", save_path)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


video.release()
cv2.destroyAllWindows()


