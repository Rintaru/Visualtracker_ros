#!/home/sekiro/final_year_ws/py2.7env/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#standard ros imports
import roslib
import rospy
import rospkg
#ros msgs to be used
from geometry_msgs.msg import Vector3Stamped 
from sensor_msgs.msg import Image
#imports for visual tracking
import cv2
from cv_bridge import CvBridge
from siamfc_test.SiameseTracker import SiameseTracker

class tracking_algorithim():
    def __init__(self):
        self.bridge = CvBridge()
        #initialise node
        rospy.init_node('siamfc_node',anonymous=False)
        #initialise publisher
        self.tgt_heading_pub = rospy.Publisher('tgt_heading',Vector3Stamped,queue_size=10)
        self.PubRate = rospy.Rate(10)#defining the rate at which we publish target headings, 10hz
        self.tgt_heading=Vector3Stamped()#this was defined here so that it would only be initialized once to avoid memory issues
        #initialise subscriber
        rospy.Subscriber('/cv_camera/image_raw',Image,self.subscriber_callback)


        self.publish()#this needs to be removed after testing

        #loading model
        rospackage = rospkg.RosPack()
        model_path = rospackage.get_path('siamfc_test')+'/scripts/siamfc_test/Logs/SiamFC/track_model_checkpoints/SiamFC-3s-color-pretrained'
        self.tracker = SiameseTracker(debug=0, checkpoint=model_path)
        print("yeet?")

        #load image and init tracker. This might have to be moved to a separate node. beccause the siamFC node will be the only node that is in the docker 
        tracker_tgt_path = rospackage.get_path('siamfc_test') + '/tracker_tgt.png'
        tracker_tgt=cv2.imread(tracker_tgt_path)
        ##uncomment for debugging purposes
        #cv2.imshow('tgt',tracker_tgt)
        #cv2.waitKey(100)
        
        #Setting the bounding box to the entire FOV of the camera to search for the target upon initialization. This should be updated beccause it might not work.
        r=(0,0,640,480)
        self.tracker.set_first_frame(tracker_tgt,r)

    def publish(self):
        self.PubRate.sleep()
        self.tgt_heading.vector.x=10
        self.tgt_heading_pub.publish(self.tgt_heading)
    
    def subscriber_callback(self,image):
        #convert image from sensor_msgs/Image to cv::mat
        cv_image = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr16')
        ##uncomment for debugging purposes
        #cv2.imshow('camera',cv_image)
        #print(type(cv_image))
        #print('\n')
        #print(cv_image.shape)
        #cv2.waitKey(1)

if __name__ == '__main__':
    try:
        tracking_algorithim()
        print("yeet!")
        rospy.spin()
        print("\nI am ded")
    except rospy.ROSInterruptException:
        pass