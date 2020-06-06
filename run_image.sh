#!/bin/bash
sudo docker kill /ros-tensorflow	#closing the terminal for a running container does not stop it. This command makes sure that the container is closed before it is started again. Usually not needed																															
sudo docker run --name ros-tensorflow --gpus all -it --rm --network host -v ~/leader_follower_ws:/workspace/leader_follower_ws ros-tensorflow:test