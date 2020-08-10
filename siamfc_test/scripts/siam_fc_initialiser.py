#! /usr/bin/env python
r"""This node outputs the image that is used to initialise the visual tracker."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#standard ros imports
import roslib
import rospy
import rospkg
#ros msgs to be used
from sensor_msgs.msg import Image
#ros service to be used
from siamfc_test.srv import img_bb_srv, img_bb_srvResponse, img_bb_srvRequest
#imports for initialising the image
import cv2
from cv_bridge import CvBridge
import numpy as np

class tracking_algorithim():
    def __init__(self):
        self.bridge = CvBridge()
        rospy.init_node('siamfc_initialiser',anonymous=False)
        #initialise subscriber to cv_camera_node
        rospy.Subscriber('/input_image_topic',Image,self.subscriber_callback, queue_size=2)
    
    def subscriber_callback(self,image):
        #convert received image from sensor_msgs/Image to cv::mat
        self.cv_tgt_image = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr16')
        self.cv_tgt_image = self.preprocess(self.cv_tgt_image)
        #make the sensor_msgs/Image version of tgt_image accesible
        self.ros_tgt_image = image



        ##uncomment for debugging purposes
        #cv2.imshow('camera',self.cv_tgt_image)
        #print(type(self.cv_tgt_image))
        #print('\n')
        #print(self.cv_tgt_image.shape)
        #cv2.waitKey(1)
    
    def preprocess(self,img):
        res = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return res
    def postprocess(self,img):
        res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return res

def call_service(image,bbox):
    try:
        s=rospy.ServiceProxy('init_img',img_bb_srv)
        s.call(img=image,bb=bbox)
        print('ended')
    except rospy.ServiceException, e:
        print('Service call failed')
            
if __name__ == '__main__':
    track=tracking_algorithim()
    print('waiting for init_img service')
    rospy.wait_for_service('init_img')
    print('init_img service has been advertised \ngrabbing an initial image')

    while not rospy.is_shutdown():
        try:
            cv2.imshow('press o to select initial frame', track.postprocess(track.cv_tgt_image))
            selected_image=[track.cv_tgt_image, track.ros_tgt_image]
            if cv2.waitKey(50) & 0xFF == ord('o'):
                boundingbox = cv2.selectROI(track.postprocess(selected_image[0]))
                print('bounding box',boundingbox)
                break
        except AttributeError:
            #An attribute error occurs when calling track.cv_tgt_image before the subscriber_callback is called.
            #Cause is cv_tgt_image attribute is created inside subscriber_callback
            #This exception is used to give subscriber_callback time to run
            print("...")
            rospy.sleep(.5)
            pass
    
    call_service(selected_image[1],boundingbox)

    cv2.destroyAllWindows()
    
    rospy.spin()
