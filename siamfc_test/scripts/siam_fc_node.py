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
#imports for visual tracking
import cv2
from siamfc_test.SiameseTracker import SiameseTracker

class tracking_algorithim():
    def __init__(self):
        self.tgt_heading_pub = rospy.Publisher('tgt_heading',Vector3Stamped,queue_size=10)

        rospy.init_node('siamfc_node',anonymous=False)

        self.PubRate = rospy.Rate(10)#defining the rate at which we publish target headings, 10hz
        self.tgt_heading=Vector3Stamped()#this was defined here so that it would only be initialized once to avoid memory issues
        self.publish()#this needs to be removed after testing
        print("yeet?")

    def publish(self):
        self.PubRate.sleep()
        self.tgt_heading.vector.x=0
        self.tgt_heading_pub.publish(self.tgt_heading)

if __name__ == '__main__':
    try:
        tracking_algorithim()
        print("yeet!")
        rospy.spin()
        print("\nI am ded")
    except rospy.ROSInterruptException:
        pass