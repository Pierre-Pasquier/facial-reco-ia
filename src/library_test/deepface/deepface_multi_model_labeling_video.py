from deepface import DeepFace
import cv2
import numpy as np
import sys, time, math
from  collections import deque
import time
import os



directory = os.getcwd() + '/src/library_test/deepface/videos_test/'



video_name = 'Crowd walking on street cropped.mp4'





video = cv2.VideoCapture(directory + video_name)

# Initialize some variables
face_locations = []

length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(video.get(3)) 
frame_height = int(video.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter(directory + 'labelled_videos/' + video_name[:-4] + '_labelled.mp4',  
                        cv2.VideoWriter_fourcc(*'mp4v'), 
                        30, size)

ret = True
current_frame = 0

# Define color codes for each model
color_codes = {
    'opencv': (0, 0, 255),       # Red
    'ssd': (255, 0, 0),          # Blue
    'mtcnn': (0, 255, 0),        # Green
    'retinaface': (255, 255, 0),  # Cyan
    'dlib': (0, 255, 255)        # Yellow
}

# Initialize legend text
legend_text = "OpenCV: Red / SSD: Blue / MTCNN: Green / RetinaFace: Cyan / Dlib: Yellow"

time_opencv = 0
time_ssd = 0
time_mtcnn = 0
time_retina = 0
time_dlib = 0

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
    start_opencv = time.time()
    try :
        face_locations_opencv = DeepFace.represent(frame, detector_backend = 'opencv')
    except :
        face_locations_opencv = []
    time_opencv += time.time() - start_opencv
    start_ssd = time.time()
    try :
        face_locations_ssd = DeepFace.represent(frame, detector_backend = 'ssd')
    except :
        face_locations_ssd = []
    time_ssd += time.time() - start_ssd
    start_mtcnn = time.time()
    try :
        face_locations_mtcnn = DeepFace.represent(frame, detector_backend = 'mtcnn')
    except :
        face_locations_mtcnn = []
    time_mtcnn += time.time() - start_mtcnn
    start_retina = time.time()
    try :
        face_locations_retina = DeepFace.represent(frame, detector_backend = 'retinaface')
    except :
        face_locations_retina = []
    time_retina += time.time() - start_retina
    start_dlib = time.time()
    try :
        face_locations_dlib = DeepFace.represent(frame, detector_backend = 'Dlib')
    except :
        face_locations_dlib = []
    time_dlib += time.time() - start_dlib



    if len(face_locations_opencv) != 0 :
        for k in range(len(face_locations_opencv)):
            x,y,w,h = face_locations_opencv[k]['facial_area']['x'], face_locations_opencv[k]['facial_area']['y'], face_locations_opencv[k]['facial_area']['w'], face_locations_opencv[k]['facial_area']['h']
            
            # Draw a box around the face
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 2)

    if len(face_locations_ssd) != 0 :
        for k in range(len(face_locations_ssd)):
            x,y,w,h = face_locations_ssd[k]['facial_area']['x'], face_locations_ssd[k]['facial_area']['y'], face_locations_ssd[k]['facial_area']['w'], face_locations_ssd[k]['facial_area']['h']
            
            # Draw a blue box around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    if len(face_locations_mtcnn) != 0 :
        for k in range(len(face_locations_mtcnn)):
            x,y,w,h = face_locations_mtcnn[k]['facial_area']['x'], face_locations_mtcnn[k]['facial_area']['y'], face_locations_mtcnn[k]['facial_area']['w'], face_locations_mtcnn[k]['facial_area']['h']
            
            # Draw a box around the face
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)
    if len(face_locations_retina) != 0 :
        for k in range(len(face_locations_retina)):
            x,y,w,h = face_locations_retina[k]['facial_area']['x'], face_locations_retina[k]['facial_area']['y'], face_locations_retina[k]['facial_area']['w'], face_locations_retina[k]['facial_area']['h']
            
            # Draw a box around the face
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 255, 0), 2)
    
    if len(face_locations_dlib) != 0 :
        for k in range(len(face_locations_dlib)):
            x,y,w,h = face_locations_dlib[k]['facial_area']['x'], face_locations_dlib[k]['facial_area']['y'], face_locations_dlib[k]['facial_area']['w'], face_locations_dlib[k]['facial_area']['h']
            
            # Draw a box around the face
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 255), 2)

    print(time.time() - start)

    # Add legend text to the frame
    cv2.putText(frame, legend_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Write the frame to the result video
    result.write(frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

mean_time_opencv = time_opencv / length
mean_time_ssd = time_ssd / length
mean_time_mtcnn = time_mtcnn / length
mean_time_retina = time_retina / length
mean_time_dlib = time_dlib / length

# Release handle to the webcam
video.release()
result.release()
cv2.destroyAllWindows()


text_width, text_height = cv2.getTextSize(legend_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
text_x = frame.shape[1] - text_width - 10
text_y = frame.shape[0] - text_height - 10
# Write time results one the video
while ret :
    # Grab a single frame of video
    ret, frame = video.read()

    # Add legend text to the frame
    cv2.putText(frame, legend_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Write the frame to the result video
    result.write(frame)

    try:
        cv2.imshow('Video', frame)
    except:
        print("Video ended")
        pass

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
video.release()
result.release()
cv2.destroyAllWindows()


