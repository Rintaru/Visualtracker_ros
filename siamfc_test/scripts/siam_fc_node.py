#!/home/sekiro/final_year_ws/py2.7env/bin/python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import roslib
import rospy
import rospkg

import logging
import os
import os.path as osp
import sys
from glob import glob

import tensorflow as tf

CURRENT_DIR = osp.dirname(__file__)
sys.path.append(osp.join(CURRENT_DIR, 'src/..'))

from siamfc_test import SiameseTracker
from inference.tracker import Tracker
from utils.infer_utils import Rectangle
from utils.misc_utils import auto_select_gpu, mkdir_p, sort_nicely, load_cfgs
print("all imports succeded")