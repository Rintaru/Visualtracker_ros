# This is an auto generated Dockerfile for ros:ros-core
# generated from docker_images/create_ros_core_image.Dockerfile.em
#FROM tensorflow/tensorflow:1.4.0-gpu
FROM nvcr.io/nvidia/tensorflow:18.02-py2

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
    ros-kinetic-cv-bridge\
    && rm -rf /var/lib/apt/lists/*

# install additional packages
RUN apt-get update && apt-get install -y \
    openssh-client \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*
#installing siamfc dependencies
RUN pip install tensorflow-gpu==1.4.0 \
    scipy \
    sacred==0.7.5 \
    matplotlib \
    opencv-python \
    pillow \
    nvidia-ml-py
# setup entrypoint
COPY ./ros_entrypoint.sh /
RUN echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc

RUN echo "printf \"\nctrl-d if you want to exit container\n\n\"" >> ~/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]