from threading import Thread
import gi
from time import sleep
import numpy as np
import sys
import face_recognition
import cv2
import matplotlib.pyplot as plt
import pandas as pd

classes = None
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# read pre-trained model and config file
net = cv2.dnn.readNet('yolov3-spp.weights', 'yolov3-spp.cfg')

# choose the numero of camera in argument if there are more than one, default 0 
args = sys.argv[1:]
num_cam = '0' if not args else args.pop(0)
if num_cam not in set('0123'):
    print("Bad camera num, must be 0,1,2  or 3")
    exit()

# clear the stdout
print("\33c")


def convert_sample_to_image(sample):
    # get the image data from a sample and return it as a numpy array
    caps = sample.get_caps()
    buf = sample.get_buffer()
    H, W, C = caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3
    image = np.ndarray((H, W, C),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
    return image

def print_image(image,N=20,boxes=[]):
    # display an image on the stdout with a reduction of N 
    print('\33c')
    H,W = image.shape[:2]
    for i in range(1,H,N):
        for j in range(1,W,N):
            if boxes and sum([pixelin([i,j],l) for l in boxes]): 
                r,g,b=image[i,j]
                print(f"\33[{i//N};{(j*2)//N}H\33[48;2;{r};{g};{b}m  \33[0m")
def pixelin(p,box):
   x = box[0]
   y = box[1]
   w = box[2]
   h = box[3]
   return abs(p[0]-x) <= w/2 and abs(p[1]-y) <= h/2



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
pipeline = Gst.parse_launch(f"v4l2src device=/dev/video{num_cam} ! decodebin ! videoconvert ! video/x-raw, format=RGB ! appsink name=sink")
# get the output video stream in the SYNC variable and start the pipeline
SYNC = pipeline.get_by_name("sink")
pipeline.set_state(Gst.State.PLAYING)
###


### IMAGE PROCESSING LOOP ###
for i in range(1000):
    # get a sample from SYNC output
    sample = SYNC.try_pull_sample(Gst.SECOND)
    boxes=[]
    if sample is not None : 
        # get the image as a numpy array from the sample
        image = convert_sample_to_image(sample)
        image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
        Width = image.shape[1]
        Height = image.shape[0]
        if 1 or i%10 == 0:
        # create input blob
        # set input blob for the network
            net.setInput(cv2.dnn.blobFromImage(image, 0.00392, (416,416), (0,0,0), True, crop=False))
    
        # run inference through the network
        # and gather predictions from output layers
    
            layer_names = net.getLayerNames()
            output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
            outs = net.forward(output_layers)
        
            class_ids = []
            confidences = []
            boxes = []
        
            #create bounding box
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.1:
                        center_x = int(detection[0] * Width)
                        center_y = int(detection[1] * Height)
                        w = int(detection[2] * Width)
                        h = int(detection[3] * Height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])
    
        # display the image on the stdout
        print_image(image,20,boxes)

#        rgb_small_frame = image[:, :, ::-1]
        #print(face_recognition.face_locations(small_image))
###
        print(boxes)

# close the pipeline and finish the programm properly 
pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()




