final year project

overlaying multiple workspace.

Traditionally, you can only run ros-packages from one workspace at a time. The steps below allow you to run ros-packages from more than one workspace 

  - cd first_layer_ws
  - catkin_make
  - cd second_layer_ws
  - source /path_to_first_layer_ws/first_layer_ws/devel/setup.bash
  - catkin_make
  - source devel/setup.bash
The steps above need to be repeated whenever catkin_make has to be performed for either workspace


T-265 test launch procedures
 - sudo apt-get install ros-melodic-realsense2-camera
 - follow the instruction on  the link for installing Realsense SDK 2.0 https://github.com/IntelRealSense/librealsense/blob/development/doc/distribution_linux.md
    - plug in your depth camera then use the 'realsense-viewer' command to test realsense camera
 
