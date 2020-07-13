#!/bin/bash
set -e
# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
cd /home/user/leader_follower_ws
catkin_make
source /home/user/leader_follower_ws/devel/setup.bash
roslaunch image_proc_fisheye image_rectification_fisheye.launch
exec "$@"