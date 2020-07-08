#!/bin/bash
set -e
# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
cd /home/user/leader_follower_ws
catkin_make
exec "$@"