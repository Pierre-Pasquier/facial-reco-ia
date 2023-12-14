import cv2
import numpy as np
import sys, time, math
from  collections import deque
import time
import os



directory = os.getcwd() + '/src/library_test/deepface/videos_test/labelled_videos/'



video_name = 'Crowd walking on street cropped_labelled.mp4'


video = cv2.VideoCapture(directory + video_name)


frame_width = int(video.get(3)) 
frame_height = int(video.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter(directory + video_name[:-4] + '_legended.mp4',
                        cv2.VideoWriter_fourcc(*'mp4v'),
                        30, size) 

ret = True
current_frame = 0


text_x = 10
text_y = frame_height - 50

# Initialize legend text
legend_text = "OpenCV: " + str(round(1.7248, 2)) + "s/SSD: " + str(round(0.3799, 2)) + "s/MTCNN: " + str(round(5.25523, 2)) + "s/RetinaFace: " + str(round(10.15370509, 2)) + "s/Dlib: " + str(round(0.00012236, 2)) + "s"




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


