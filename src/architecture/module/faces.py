from threading import Thread
import gi
from time import sleep
import numpy as np
import sys
import dlib
import cv2
import time
#import face_recognition

# choose the numero of camera in argument if there are more than one, default 0 
args = sys.argv[1:]
num_cam = '0' if not args else args.pop(0)
if num_cam not in set('0123'):
    print("Bad camera num, must be 0,1,2  or 3")
    exit()

face_detector = "models/mmod_human_face_detector.dat"

# clear the stdout
#print("\33c")

def save_cropped_faces(faces, image, frame, qf):
    # qf = quality_factor
    # Save cropped faces as separate images in a directory
    for i, face in enumerate(faces):
        #print(face)
        (x, y, w, h) = (int(face.rect.left()/qf), int(face.rect.top()/qf), int(face.rect.width()/qf), int(face.rect.height()/qf))
        cropped_face = image[y:y+h, x:x+w]
        try:
            cv2.imwrite(f"images/temp/face_{i}_frame_{frame}.jpg", cropped_face)
        except:
            pass


def convert_sample_to_image(sample):
    # get the image data from a sample and return it as a numpy array
    caps = sample.get_caps()
    buf = sample.get_buffer()
    H, W, C = caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3
    image = np.ndarray((H, W, C),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
    return image

 
def main(quality_factor=0.3):
    ### GSTREAMER IMPORT ###
    gi.require_version('Gst','1.0')
    gi.require_version('GstApp','1.0')
    
    from gi.repository import Gst,GLib,GstApp
    ###
    
    
    ### INIT GSTREAMER DEAMON ###
    Gst.init()
    
    main_loop = GLib.MainLoop()
    main_loop_thread = Thread(target=main_loop.run)
    main_loop_thread.start()
    ###
    
    
    ### GSTREAMER PIPELINE ###
    # Finish on appsink to handle the output video stream in the python programm 
    pipeline = Gst.parse_launch(f"v4l2src device=/dev/video{num_cam} ! decodebin ! videoconvert ! video/x-raw,format=RGB ! appsink name=sink")
    # get the output video stream in the SYNC variable and start the pipeline
    SYNC = pipeline.get_by_name("sink")
    pipeline.set_state(Gst.State.PLAYING)
    ###

    detector = dlib.cnn_face_detection_model_v1(face_detector)

    ### IMAGE PROCESSING LOOP ###
    flag = 0
    for i in range(100):
        start = time.time()
        # get a sample from SYNC output
        sample = SYNC.try_pull_sample(Gst.SECOND)
        if sample is not None : 
            # get the image as a numpy array from the sample
            image = convert_sample_to_image(sample)
            image = image[:, :, ::-1]
            small_image = cv2.resize(image, (0,0), fx=quality_factor, fy=quality_factor)
            faces_detected = detector(small_image, 1)
            #print(len(faces_detected))
            if len(faces_detected) != 0:
                save_cropped_faces(faces_detected, image, i, quality_factor)
                #print("image saved")
                flag = 1
                #exit(1)
            #print(faces_detected)
        #print(f"FPS: {1/(time.time() - start)}")
    ###
    print(flag)


    # close the pipeline and finish the programm properly 
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
    main_loop_thread.join()
    
if __name__ == "__main__":
    main()
