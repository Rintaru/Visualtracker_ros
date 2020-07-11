#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.
r"""Visual tracking node."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#standard ros imports
import roslib
import rospy
import rospkg
import os
#ros msgs to be used
from geometry_msgs.msg import Vector3Stamped 
from sensor_msgs.msg import Image
#ros service to be used
from siamfc_test.srv import img_bb_srv, img_bb_srvResponse, img_bb_srvRequest
#imports for visual tracking
import cv2
from cv_bridge import CvBridge
from siam_fc.SiameseTracker import SiameseTracker

class tracking_algorithim():
    def __init__(self):
        self.bridge = CvBridge()
        
        #load model used by visual tracker
        rospackage = rospkg.RosPack()
        model_path = rospackage.get_path('siamfc_test')+'/scripts/siam_fc/Logs/SiamFC/track_model_checkpoints/SiamFC-3s-color-pretrained'
        self.tracker = SiameseTracker(debug=0, checkpoint=model_path)
        
        #initialise node
        rospy.init_node('siamfc_node',anonymous=False)
        
        #initialise publisher
        self.tgt_heading_pub = rospy.Publisher('tgt_heading',Image,queue_size=10)
        self.PubRate = rospy.Rate(10)#defining the rate at which we publish target headings, 10hz
        self.tgt_heading=Image()#this was defined here so that it would only be initialized once to avoid memory issues
        
        self.init_service()

        self.init_subscriber()
        self.after=rospy.Time.now().to_sec()*1000
        self.before=rospy.Time.now().to_sec()*1000

        print("yeet?")

    #function used to publish the tgt's location
    def publish(self,target_image):
        self.tgt_heading=self.bridge.cv2_to_imgmsg(target_image, encoding="rgb8")
        self.PubRate.sleep()
        self.tgt_heading_pub.publish(self.tgt_heading)
    
    def subscriber_callback(self,image):
        self.after=rospy.Time.now().to_sec()*1000
        print("time since callback was called",(self.after-self.before),"mS","\n")
        
        self.before=rospy.Time.now().to_sec()*1000
        #convert received image from sensor_msgs/Image to cv::mat
        cv_image = self.bridge.imgmsg_to_cv2(image, desired_encoding='rgb8')
        self.after=rospy.Time.now().to_sec()*1000
        print("time to convert ros_image to cv_image",(self.after-self.before),"mS","\n")

        self.before=rospy.Time.now().to_sec()*1000
        #actual tracking of the target occurs here
        reported_bbox = self.tracker.track(cv_image)
        self.after=rospy.Time.now().to_sec()*1000
        print("time to track tgt",(self.after-self.before),"mS","\n")

        self.before=rospy.Time.now().to_sec()*1000
         #draw a bounding box on the target
        cv2.rectangle(cv_image, (int(reported_bbox[0]), int(reported_bbox[1])),
                      (
                          int(reported_bbox[0]) + int(reported_bbox[2]),
                          int(reported_bbox[1]) + int(reported_bbox[3])),
                      (0, 0, 255), 2)
        self.after=rospy.Time.now().to_sec()*1000
        print("time to draw tgt image",(self.after-self.before),"mS","\n")
        
        self.before=rospy.Time.now().to_sec()*1000
        self.publish(cv_image)
        self.after=rospy.Time.now().to_sec()*1000
        print("time to publish tgt image",(self.after-self.before),"mS","\n")

        os.system('cls' if os.name == 'nt' else 'clear')
        self.before=rospy.Time.now().to_sec()*1000
    
    #Used for debugging purposes
    def display_image(im):
        cv2.imshow('camera',im)
        print(type(im))
        print('\n')
        print(im.shape)
        cv2.waitKey(1)

    
    #image to initialise the tracker is received here.
    def service_handle(self,init_img):
        #convert initial image in to cv::mat
        cv_init_img=self.bridge.imgmsg_to_cv2(init_img.img)
        self.tracker.set_first_frame(cv_init_img,init_img.bb)
        #setting this bool to True will allow this node to subscribe to cv_camera
        self.is_tracker_init=True
        return img_bb_srvResponse(True)

    #initialise the service that is used to initialise or re-initialise the visual tracker
    def init_service(self):
        rospy.Service('init_img',img_bb_srv,self.service_handle)
        self.is_tracker_init=False

    #initialise subscriber to cv_camera node
    def init_subscriber(self):
        print('waiting for initial image')
        #if the visual tracker has not received an inital image AND node has not been shutdown then block
        while not self.is_tracker_init and not rospy.is_shutdown():
            pass
        #subscribe to cv_camera node
        rospy.Subscriber('/camera_array/cam0/image_raw',Image,self.subscriber_callback, queue_size=2)



if __name__ == '__main__':
    try:
        tracking_algorithim()
        print("yeet!")
        rospy.spin()
        print("\n I am ded")
    except rospy.ROSInterruptException:
        pass
