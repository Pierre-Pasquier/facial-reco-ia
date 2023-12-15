from threading import Thread
import gi
from time import sleep
import numpy as np
import sys
import dlib
import cv2
#import face_recognition

# choose the numero of camera in argument if there are more than one, default 0 
args = sys.argv[1:]
num_cam = '0' if not args else args.pop(0)
if num_cam not in set('0123'):
    print("Bad camera num, must be 0,1,2  or 3")
    exit()

# clear the stdout
print("\33c")

def save_cropped_faces(faces, image, frame):
    # Save cropped faces as separate images in a directory
    for i, face in enumerate(faces):
        print(face)
        (x, y, w, h) = (face.left(), face.top(), face.width(), face.height())
        cropped_face = image[y:y+h, x:x+w]
        cv2.imwrite(f"../images/temp/face_{i}_frame_{frame}.jpg", cropped_face)



def convert_sample_to_image(sample):
    # get the image data from a sample and return it as a numpy array
    caps = sample.get_caps()
    buf = sample.get_buffer()
    H, W, C = caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3
    image = np.ndarray((H, W, C),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
    return image

def pixelin(p,loc):
    return p[0]>=loc[0] and p[1]>=loc[2] and p[1]<=loc[1] and p[0]<=loc[3]

def print_image(image,locations=[],N=20):
    # display an image on the stdout with a reduction of N 
    print("\33c")
    H,W = image.shape[:2]
    for i in range(1,H,N):
        for j in range(1,W,N):
            if 1 or locations and sum([pixelin([i,j],l) for l in locations]):
                r,g,b=image[i,j]
                print(f"\33[{i//N};{(j*2)//N}H\33[48;2;{r};{g};{b}m  \33[0m")
 
def main():
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
    
    detector = dlib.get_frontal_face_detector()
    
    ### IMAGE PROCESSING LOOP ###
    for i in range(1000):
        # get a sample from SYNC output
        sample = SYNC.try_pull_sample(Gst.SECOND)
        if sample is not None : 
            # get the image as a numpy array from the sample
            image = convert_sample_to_image(sample)
            image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
            faces_detected = detector(image, 1)
            if faces_detected != []:
                save_cropped_faces(faces_detected, image, i)
                print("image saved")
            print(faces_detected)    
    ###
    
    
    # close the pipeline and finish the programm properly 
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
    main_loop_thread.join()

if __name__ == "__main__":
    main()
