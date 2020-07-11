#!/bin/bash
set -e
# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
#copy leader_follower_ws into home, as it would be in host PC and echo specific commands in to bashrc
mkdir -p /home/leader_follower_ws
cp -r /workspace/leader_follower_ws/src /home/leader_follower_ws/src
#remove unneeded packages
rm -r /home/leader_follower_ws/src/t265_driver/
cd /home/leader_follower_ws
catkin_make
#standard bashrc lines for ROS
source /home/leader_follower_ws/devel/setup.bash
printf \n\nctrl-d if you want to exit container\n\n
rosrun siamfc_test siam_fc_node.py
exec "$@"