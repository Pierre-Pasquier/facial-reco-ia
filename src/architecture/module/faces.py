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

### GSTREAMER IMPORT ###
gi.require_version('Gst','1.0')
gi.require_version('GstApp','1.0')

from gi.repository import Gst,GLib,GstApp

sys.path.append(os.getcwd())


def convert_sample_to_image(sample):
    # get the image data from a sample and return it as a numpy array
    caps = sample.get_caps()
    buf = sample.get_buffer()
    H, W, C = caps.get_structure(0).get_value('height'), caps.get_structure(0).get_value('width'), 3
    image = np.ndarray((H, W, C),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
    return image


def save_cropped_faces(faces, image):
    # Save cropped faces as separate images in a directory
    for i, face in enumerate(faces):
        (x, y, w, h) = (face.rect.left(), face.rect.top(), face.rect.width(), face.rect.height())
        cropped_face = image[y:y+h, x:x+w]
        cv2.imwrite(f"../images/tmp/face_{i}.jpg", cropped_face)


def main(num_cam=0, frame_without_detection=150, face_detector="models/mmod_human_face_detector.dat"):
    print("main")
    ### INIT GSTREAMER DEAMON ###
    Gst.init(None)

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
    for i in range(frame_without_detection):
        print(f"i : {i}")
        # get a sample from SYNC output
        sample = SYNC.try_pull_sample(Gst.SECOND)
        print(sample)
        if sample is not None : 
            print("sample is not None")
            # get the image as a numpy array from the sample
            image = convert_sample_to_image(sample)
            # rgb_small_frame = image[:, :, ::-1]
            faces_detected = detector(image, 1)
            save_cropped_faces(faces_detected, image)
            print(faces_detected)
            

        ###


        # close the pipeline and finish the programm properly 
        pipeline.set_state(Gst.State.NULL)
        main_loop.quit()
        main_loop_thread.join()

if __name__ == "__main__":
    main()
