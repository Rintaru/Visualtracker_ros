#!/bin/bash
sudo docker kill /t265_driver																												
sudo docker run --name t265_driver --privileged --gpus all -it --rm --network host -v ~/leader_follower_ws:/workspace/leader_follower_ws t265_driver:test