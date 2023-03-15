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


# choose the numero of camera in argument if there are more than one, default 0 
args = sys.argv[1:]
num_cam = '0' if not args else args.pop(0)
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



def save_cropped_faces(x,y,w,h, image,i, compt):
    cropped_face = image[y:y+h, x:x+w]
    try:
        cv2.imwrite(f"images/temp/person_{i}_{compt}.jpg", cropped_face)
    except:
        pass


def exit_pipeline(pipeline, main_loop, main_loop_thread, Gst):
    # close the pipeline and finish the programm properly 
    pipeline.set_state(Gst.State.NULL)
    main_loop.quit()
    main_loop_thread.join()
    exit()

def main(num_cam=0, frame_without_detection=150, quality_factor=0.25):
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
    net = cv2.dnn.readNet('models/yolov3-spp.weights', 'models/yolov3-spp.cfg')
    

    ### IMAGE PROCESSING LOOP ###
    for i in range(frame_without_detection):
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
            net.setInput(cv2.dnn.blobFromImage(small_image, 0.00392, (416,416), (0,0,0), True, crop=False))
            # rgb_small_frame = image[:, :, ::-1]

            ### FACE DETECTION
            layer_names = net.getLayerNames()
            output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
            persons_detected = net.forward(output_layers)
            ###
            #print(persons_detected)
            #Width = image.shape[1]
            #Height = image.shape[0]
            for person_detected in persons_detected :
                #compt = 0
                for detection in person_detected :
                    #compt += 1
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.1 and class_id == 0 :
                        #print("condidence " + str(confidence))
                        #print("class_id : " + str(classes[class_id]), class_id)
                        #c_x = int(detection[0] * Width)
                        #c_y = int(detection[1] * Height)
                        #w = int(detection[2] * Height)
                        #h = int(detection[3] * Height)
                        #x = int(c_x - w/2)
                        #y = int(c_y - h/2)
                        #save_cropped_faces(x,y,w,h,image,i, compt)
                        print("1")
                        exit_pipeline(pipeline, main_loop, main_loop_thread, Gst)
                        
                #print("FPS : " + str(1/(time.time() - start)))
            

        ###

    print("0")
    exit_pipeline(pipeline, main_loop, main_loop_thread, Gst)

if __name__ == "__main__":
    main()

