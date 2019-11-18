# Import the camera server
from cscore import CameraServer

# Import OpenCV and NumPy
import cv2
import numpy as np


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    # Capture from the first USB Camera on the system
    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Name", 320, 240)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)

        img_blur = cv2.blur(img, (5, 5))
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        lower_range = np.array([30, 150, 50])
        upper_range = np.array([255, 255, 180])
        mask = cv2.inRange(img_hsv, lower_range, upper_range)
        res = cv2.bitwise_and(img, img, mask=mask)
        img2, contours, hierarchy = cv2.findContours(
            res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(contours)

        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue

        #
        # Insert your image processing logic here!
        #

        # (optional) send some image back to the dashboard
        outputStream.putFrame(img)


main()
