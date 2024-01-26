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

# choose the numero of camera in argument if there are more than one, default 0 
#args = sys.argv[1:]
num_cam = '0' # if not args else args.pop(0)
if num_cam not in set('0123'):
    print("Bad camera num, must be 0,1,2  or 3")
    exit()

# Function to convert the gstreamer sample to an image
def convert_sample_to_image(sample):
    # get the image data from a sample and return it as a numpy array
    caps = sample.get_caps()
    buf = sample.get_buffer()
    H, W, C = caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3
    image = np.ndarray((H, W, C),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
    return image
    
# Function to exit the gstreamer pipeline properly
def exit_pipeline(pipeline, main_loop, main_loop_thread, Gst):
    # close the pipeline and finish the programm properly 
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
    main_loop_thread.join()
    exit()


@click.command()
@click.option('--num_cam', type=int, help='Choose the numero of the camera you want to use', required=False, default=0)
@click.option('--verbose', '-v', is_flag=True, help='Activate the verbose', required=False)
@click.option('--frame_without_detection', type=int, help='Number of frame without detection this script run before exiting', required=False, default=150)
@click.option('--quality_factor', type=float, help='Multiply the image quality by this factor', required=False, default=0.25)
def main(num_cam, verbose, frame_without_detection, quality_factor):
    ### GSTREAMER IMPORT ###
    if verbose :
        print("Starting imports ...")
        start_import = time.time()
    gi.require_version('Gst','1.0')
    gi.require_version('GstApp','1.0')
    from gi.repository import Gst,GLib,GstApp
    
    ### YOLO IMPORT
    from ultralytics import YOLO
    
    if verbose :
        print(f"Time for imports : {time.time() - start_import}")
    ###
    
    
    ### INIT GSTREAMER DEAMON ###
    if verbose :
        print("Launching Gstreamer pipeline ...")
        start_gstreamer = time.time()
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
    
    if verbose :
        print(f"Time to launch Gstreamer : {time.time() - start_gstreamer}")
    ###

    ### LOAD MODEL
    if verbose :
        print("Loading model ...")
        start_model = time.time()
    
    # The model used is Yolov8
    model = YOLO("models/yolov8n.pt")
    
    if verbose :
        model.predict("bus.jpg", verbose = False)
        print(f"Time to load model : {time.time() - start_model} \n\n\n\n")

    ### IMAGE PROCESSING LOOP ###
    while True:
        start = time.time()
        
        # get a sample from SYNC output
        sample = SYNC.try_pull_sample(Gst.SECOND)

        if sample is not None : 
            # get the image as a numpy array from the sample
            image = convert_sample_to_image(sample)
            
            # reduce the quality of the image to go faster
            small_image = cv2.resize(image, (0,0), fx=quality_factor, fy=quality_factor)
            
            if verbose :
                print("\33[5A")
                
            # predict if their is people on the image
            persons_detected = model.predict(image, classes=0, verbose=verbose)

            # if their are people on the image
            if len(persons_detected[0].boxes) > 0 :
                # return 1 on the stderr
                print("1", file=sys.stderr)
                
                # exit pipeline properly
                exit_pipeline(pipeline, main_loop, main_loop_thread, Gst)


if __name__ == "__main__":
    main()

