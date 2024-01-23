import os
import sys
import numpy as np
from threading import Thread
import gi
from time import sleep
import numpy as np
import sys
import dlib
import cv2
import time
import click
from ultralytics import YOLO


# choose the numero of camera in argument if there are more than one, default 0 
#args = sys.argv[1:]
num_cam = '0' # if not args else args.pop(0)
if num_cam not in set('0123'):
    print("Bad camera num, must be 0,1,2  or 3")
    exit()

# clear the stdout
#print("\33c")


#classes = None
#with open('../../../models/coco.names','r') as f:
#    classes = [line.strip() for line in f.readlines()]


def convert_sample_to_image(sample):
    # get the image data from a sample and return it as a numpy array
    caps = sample.get_caps()
    buf = sample.get_buffer()
    H, W, C = caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3
    image = np.ndarray((H, W, C),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
    return image




def exit_pipeline(pipeline, main_loop, main_loop_thread, Gst):
    # close the pipeline and finish the programm properly 
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
    main_loop_thread.join()
    exit()



@click.command()
@click.option('--num_cam', type=int, help='Choose the numero of the camera you want to use', required=False, default=0)
@click.option('--verbose', '-v', is_flag=True, type=float, help='Activate the verbose', required=False)
@click.option('--frame_without_detection', type=int, help='Number of frame without detection this script run before exiting', required=False, default=150)
@click.option('--quality_factor', type=float, help='Multiply the image quality by this factor', required=False, default=0.25)
def main(num_cam, verbose, frame_without_detection, quality_factor):
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

    ### LOAD MODEL
    model = YOLO("yolov8n.pt")
    

    ### IMAGE PROCESSING LOOP ###
    while True:
        start = time.time()
        #print(f"i : {i}")
        # get a sample from SYNC output
        sample = SYNC.try_pull_sample(Gst.SECOND)
        #print(sample)
        if sample is not None : 
            #print("sample is not None")
            # get the image as a numpy array from the sample
            image = convert_sample_to_image(sample)
            small_image = cv2.resize(image, (0,0), fx=quality_factor, fy=quality_factor)
            persons_detected = model.predict(image, classes=0)
            # rgb_small_frame = image[:, :, ::-1]




            if len(persons_detected[0].boxes) > 0 :
                print("1", file=sys.stderr)
                exit_pipeline(pipeline, main_loop, main_loop_thread, Gst)
                        
                #print("FPS : " + str(1/(time.time() - start)))
            

        ###

if __name__ == "__main__":
    main()

