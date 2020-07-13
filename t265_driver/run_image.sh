#!/bin/bash
sudo docker kill /t265_driver																												
sudo docker run --name t265_driver --privileged --gpus all -it --rm --network host -v /dev/:/dev/ t265_driver:test