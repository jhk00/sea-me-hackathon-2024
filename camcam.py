#!/usr/bin/env python

# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge
import cv2
import numpy as np

steering_weight = 1.5 
throttle_weight = 0.1 

pub_steering = rospy.Publisher('/Steering', Float32, queue_size=1)
pub_throttle = rospy.Publisher('/Throttle', Float32, queue_size=1)

gijun = 30000
cntgijun = 1
flag_line = True
flag_throttle = True
pre_lineDetect = 0
class CameraDisplay:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)

        # Create trackbars for adjusting HSV threshold values
        cv2.namedWindow("Thresholded Image")
        cv2.createTrackbar("Hue Min", "Thresholded Image", 0, 180, self.update_threshold)
        cv2.createTrackbar("Hue Max", "Thresholded Image", 180, 180, self.update_threshold)
        cv2.createTrackbar("Sat Min", "Thresholded Image", 0, 255, self.update_threshold)
        cv2.createTrackbar("Sat Max", "Thresholded Image", 255, 255, self.update_threshold)
        cv2.createTrackbar("Val Min", "Thresholded Image", 250, 255, self.update_threshold)
        cv2.createTrackbar("Val Max", "Thresholded Image", 255, 255, self.update_threshold)

        self.lower_hsv = np.array([0, 0, 250])
        self.upper_hsv = np.array([255, 255, 255])
        self.throttle_value = 0.1

    def update_threshold(self, _):
        self.lower_hsv = np.array([cv2.getTrackbarPos("Hue Min", "Thresholded Image"),
                                  cv2.getTrackbarPos("Sat Min", "Thresholded Image"),
                                  cv2.getTrackbarPos("Val Min", "Thresholded Image")])
        self.upper_hsv = np.array([cv2.getTrackbarPos("Hue Max", "Thresholded Image"),
                                  cv2.getTrackbarPos("Sat Max", "Thresholded Image"),
                                  cv2.getTrackbarPos("Val Max", "Thresholded Image")])

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            rospy.logerr("CvBridge Error: {}".format(e))
            return

        # Convert the image to HSV
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Apply the threshold to the HSV image
        thresholded_image = cv2.inRange(hsv_image, self.lower_hsv, self.upper_hsv)
        # rospy.loginfo("thresholded_image: {}".format(thresholded_image))
        # result = cv2.bitwise_and(frame, frame, thresholded_image=thresholded_image)
        # sum
        # Calculate the area of the left and right regions
        h, w = thresholded_image.shape
        wvX = np.arange(0, w)
        wvY1 = np.arange(0, h)
        wvY = (wvY1.reshape(480, 1)) / 10
        wvXX = wvX - (w / 2)
        tresh = thresholded_image / 255

        tresh12 = tresh * wvXX
        lineDetect = np.sum(tresh12)
        global flag_line
        global flag_throttle
        pre_lineDetect = np.sum(tresh12)

        if flag_line == True:
            pre_lineDetect = lineDetect
            rospy.loginfo("pre_lineDetect: {}".format(pre_lineDetect))
            flag_line = False

        if lineDetect > 500000:
            rospy.loginfo("lineDetect: {}".format("right"))
            pub_steering.publish(1)
        elif lineDetect < -500000:
            rospy.loginfo("lineDetect: {}".format("Left"))
            pub_steering.publish(-1)
        else:
            rospy.loginfo("lineDetect: {}".format("gogo"))
            normalized_value = lineDetect / 500000.0
            rospy.loginfo("lineDetect: {}".format(normalized_value))
            pub_steering.publish(normalized_value)


        if flag_throttle == True:
            if (abs(pre_lineDetect) - abs(lineDetect)) < 500:
                self.throttle_value = self.throttle_value + 0.01
        else:
            flag_throttle = False
            
        pub_throttle.publish(self.throttle_value)

        rospy.loginfo("lineDetect: {}".format(lineDetect))

        # Display the original, HSV, and thresholded images
        cv2.imshow("Camera Image", cv_image)
        cv2.imshow("HSV Image", hsv_image)
        cv2.imshow("Thresholded Image", thresholded_image)
        cv2.waitKey(1)

def shutdown_hook():
    pub_throttle.publish(0.0)
    rospy.loginfo("Shutdown: Throttle set to 0.0")

def main():
    rospy.init_node('camera_display', anonymous=True)
    rospy.on_shutdown(shutdown_hook)
    CameraDisplay()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

