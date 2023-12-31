from deepface import DeepFace
import cv2
import numpy as np
import sys, time, math
from  collections import deque
import time
import os




face_recognition_models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

face_detection_models = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe'
]

directory = os.getcwd() + '/data/videos_test/'
print(directory)

videos = ['Crowd walking on street.mp4',
          'Crowd of People Walking in London.mp4',
          'Crowd walking forward NYC.mp4',
          'Walking Around New York City.mp4',
          'Walking Crowd.mp4']


for vid in videos :
    time_video_start = time.time()
    for model in face_detection_models :
        time_video_model_start = time.time()
        print("Currently labelling video " + vid + " with model " + model)
        video = cv2.VideoCapture(directory + vid)

        # Initialize some variables
        face_locations = []

        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(video.get(3)) 
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)
        result = cv2.VideoWriter(directory + 'labelled_videos/' + vid[:-4] + '_labelled_' + model + '.mp4',  
                                cv2.VideoWriter_fourcc(*'mp4v'), 
                                30, size) 

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
            start = time.time()
            try :
                face_locations = DeepFace.represent(frame, detector_backend = model)
            except :
                face_locations = []
                print("No face detected")


            if len(face_locations) != 0 :
                for k in range(len(face_locations)):
                    x,y,w,h = face_locations[k]['facial_area']['x'], face_locations[k]['facial_area']['y'], face_locations[k]['facial_area']['w'], face_locations[k]['facial_area']['h']
                    
                    # Draw a box around the face
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 2)

            print(time.time() - start)

            #writer(frame, "Fps={:06.2f}".format(fps()))
            result.write(frame) 

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video.release()
        result.release()
        cv2.destroyAllWindows()
        print("Video " + vid + " labelled with model " + model + " !")
        time_video_model_end = time.time()
        f = open(directory + "time_result.txt", "a")
        f.write("Video " + vid + " labelled with model " + model + " in " + str(time_video_model_end - time_video_model_start) + " seconds for " + str(length) + " frames -> rate of " + str((time_video_model_end - time_video_model_start)/length) + " seconds per frame \n")
        f.close()

    time_video_end = time.time()
    f = open(directory + "time_result.txt", "a")
    f.write("Video " + vid + " labelled with every model in " + str(time_video_model_end - time_video_model_start) + " seconds for " + str(length) + " frames\n\n")
    f.close()
