from deepface import DeepFace
import cv2
import numpy as np
import sys, time, math
from  collections import deque


models = [
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

#face recognition
def face_recognition(image_path):
    dfs = DeepFace.find(img_path = image_path,
        db_path = "C:/Users/pierr/.deepface/database", 
        model_name = models[1]
    )
    print(dfs)


def analyze_face(image_path):
    dfs = DeepFace.analyze(img_path = image_path,
        actions = ['age', 'gender', 'race', 'emotion'] 
    )
    print(dfs)



#embeddings
def get_embeddings(image_path):
    embedding_objs = DeepFace.represent(img_path = image_path, 
        model_name = models[2]
    )
    print(embedding_objs)



class FPS (object):
    def __init__(self,avarageof=50):
        self.frametimestamps = deque(maxlen=avarageof)
    def __call__(self):
        self.frametimestamps.append(time.time())
        if(len(self.frametimestamps) > 1):
            return len(self.frametimestamps)/ \
                (self.frametimestamps[-1]-self.frametimestamps[0])
        else:
            return 0.0
        



class TextWriter(object) : 
    def __init__(self):
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._fontScale = 1
        self._fontColor = (0,0,255)
        self._lineType = 2
    def __call__(self, img, text, pos=(40,40)) :
        cv2.putText(img, text, pos, self._font, self._fontScale, self._fontColor, self._lineType)
        

def camera_analyze_test():
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    process_this_frame = True

    fps = FPS()
    writer = TextWriter()

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            try :
                face_locations = DeepFace.represent(frame, model_name = models[2])
            except :
                face_locations = []

            
        process_this_frame = not process_this_frame
        if len(face_locations) != 0 :
            for k in range(len(face_locations)):
                x,y,w,h = face_locations[k]['facial_area']['x'], face_locations[k]['facial_area']['y'], face_locations[k]['facial_area']['w'], face_locations[k]['facial_area']['h']
                
                # Draw a box around the face
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 2)


        writer(frame, "Fps={:06.2f}".format(fps()))
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def camera_detection_test():
    video = cv2.VideoCapture('C:/Users/pierr/Desktop/Telecom_Nancy/3A/PI/Vidéos test/Crowd walking forward NYC B-Roll.mp4')

    # Initialize some variables
    face_locations = []
    process_this_frame = True

    #fps = FPS()
    #writer = TextWriter()

    frame_width = int(video.get(3)) 
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)
    result = cv2.VideoWriter('C:/Users/pierr/Desktop/Telecom_Nancy/3A/PI/Vidéos test/Result/Crowd walking forward NYC B-Roll_OpenFace.mp4',  
                            cv2.VideoWriter_fourcc(*'mp4v'), 
                            30, size) 

    ret = True

    while ret :
        # Grab a single frame of video
        ret, frame = video.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            try :
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            except :
                ret, frame = video.read()

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            try :
                face_locations_0 = DeepFace.represent(frame, model_name = models[0])
                face_locations_1 = DeepFace.represent(frame, model_name = models[1])
                face_locations_2 = DeepFace.represent(frame, model_name = models[2])
                face_locations_3 = DeepFace.represent(frame, model_name = models[3])
                face_locations_4 = DeepFace.represent(frame, model_name = models[4])
                face_locations_5 = DeepFace.represent(frame, model_name = models[5])
                face_locations_6 = DeepFace.represent(frame, model_name = models[6])
                face_locations_7 = DeepFace.represent(frame, model_name = models[7])
                face_locations_8 = DeepFace.represent(frame, model_name = models[8])
            except :
                face_locations = []

            if face_locations_0 == face_locations_1 == face_locations_2 == face_locations_3 == face_locations_4 == face_locations_5 == face_locations_6 == face_locations_7 == face_locations_8 :
                print("Les modèles trouvent les mêmes visages")
            else :
                print(face_locations_0, face_locations_1, face_locations_2, face_locations_3, face_locations_4, face_locations_5, face_locations_6, face_locations_7, face_locations_8)
            

        process_this_frame = not process_this_frame

        if len(face_locations) != 0 :
            for k in range(len(face_locations)):
                x,y,w,h = face_locations[k]['facial_area']['x'], face_locations[k]['facial_area']['y'], face_locations[k]['facial_area']['w'], face_locations[k]['facial_area']['h']
                
                # Draw a box around the face
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 2)


        #writer(frame, "Fps={:06.2f}".format(fps()))
        result.write(frame) 
        # Display the resulting image
        try:
            cv2.imshow('Video', frame)
        except:
            pass
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video.release()
    result.release()
    cv2.destroyAllWindows()