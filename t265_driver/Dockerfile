# This is an auto generated Dockerfile for ros:ros-core
# generated from docker_images/create_ros_core_image.Dockerfile.em
FROM tanmaniac/opencv3-cudagl:latest

# install packages
RUN apt-get update && apt-get install -q -y \
    dirmngr \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros1-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV ROS_DISTRO kinetic
# bootstrap rosdep
RUN rosdep init && \
  rosdep update --rosdistro $ROS_DISTRO

# install ros packages and opencv python dependencies
RUN apt-get update && apt-get install -y \
    ros-kinetic-ros-core=1.3.2-0* \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ros-kinetic-cv-bridge \
    && rm -rf /var/lib/apt/lists/*

# install additional packages
RUN apt-get update && apt-get install -y \
    openssh-client \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# install image_proc and realsense packages
RUN apt-get update && apt-get install -y \
    ros-kinetic-image-transport \
    ros-kinetic-image-geometry \
    ros-kinetic-nodelet \
    ros-kinetic-realsense2-camera\
    && rm -rf /var/lib/apt/lists/*


# setup entrypoint
COPY ./ros_entrypoint.sh /
RUN chmod +x ros_entrypoint.sh
COPY ./docker_bashrc.txt /docker_bashrc.txt
RUN echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc



ENV USERNAME user
RUN useradd -m $USERNAME && \
        echo "$USERNAME:$USERNAME" | chpasswd && \
        usermod --shell /bin/bash $USERNAME && \
        usermod -aG sudo $USERNAME && \
        echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
        chmod 0440 /etc/sudoers.d/$USERNAME && \
        # Replace 1000 with your user/group id
        usermod  --uid 1000 $USERNAME && \
        groupmod --gid 1000 $USERNAME



#copy camera driver packages into container's workspace
RUN mkdir -p /home/$USERNAME/leader_follower_ws
RUN echo "cp -r /workspace/leader_follower_ws/src /home/leader_follower_ws/src" >> ~/.bashrc
COPY ./camera_calibration_fisheye /home/$USERNAME/leader_follower_ws/src/camera_calibration_fisheye
COPY ./image_proc_fisheye /home/$USERNAME/leader_follower_ws/src/image_proc_fisheye
#set bashrc to catkin_make on startup
RUN echo "cd /home/leader_follower_ws" >> ~/.bashrc
RUN echo "catkin_make" >> ~/.bashrc
#standard bashrc lines for ROS
RUN echo "source /home/$USERNAME/leader_follower_ws/devel/setup.bash" >> ~/.bashrc
RUN echo "printf \"\nctrl-d if you want to exit container\n\n\"" >> ~/.bashrc
#restore bashrc to it's original state so that catkin_make command is not run twice.
RUN echo "mv /docker_bashrc.txt  ~/.bashrc" >> ~/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]