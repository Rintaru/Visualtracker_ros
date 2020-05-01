#!/bin/bash
																																		
docker run --name ros-tensorflow --gpus all -it --rm --network host -v ~/final_year_ws:/workspace/final_year_ws ros-tensorflow:test
