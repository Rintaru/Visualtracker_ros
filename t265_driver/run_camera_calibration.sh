#!/bin/bash
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

sudo docker kill /t265_driver																												
sudo docker run --name t265_driver --privileged --gpus all -it --rm --network host \
        --volume=$XSOCK:$XSOCK:rw \
        --volume=$XAUTH:$XAUTH:rw \
        -v ~/leader_follower_ws/src/t265_driver/calibration_data:/home/user/calibration_data \
        --env="XAUTHORITY=${XAUTH}" \
        --env="DISPLAY" \
        t265_driver:test