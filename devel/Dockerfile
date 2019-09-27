# ============================================================================
# Copyright 2019 Vassilios Tsounis. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

#==
# Foundation
#==

ARG ARCH=
ARG UBUNTU_VERSION=18.04
ARG CUDA=10.0
FROM nvidia/cuda${ARCH:+-$ARCH}:${CUDA}-base-ubuntu${UBUNTU_VERSION} as base
ARG ARCH
ARG CUDA

# Needed for string substitution
SHELL ["/bin/bash", "-c"]
ENV USER=docker
ENV TERM=xterm-256color

# Base dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    locate \
    curl \
    wget \
    git \
    unzip \
    pkg-config \
    build-essential \
    cmake \
    software-properties-common \
    vim \
    ffmpeg

#==
# Unprivileged User
#==

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN usermod -s /bin/bash docker

#==
# Python
#==

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV WORKON_HOME=/home/docker/.virtualenvs
ENV VIRTUALENVWRAPPER_PYTHON=/usr/bin/python

RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    python-virtualenv \
    python3 \
    python3-pip \
    python3-virtualenv

RUN pip --no-cache-dir install -U virtualenvwrapper
USER docker:docker
RUN source /usr/local/bin/virtualenvwrapper.sh
RUN echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
RUN python -m virtualenv --python=/usr/bin/python3 /home/docker/.virtualenvs/tensorflow
USER root

#==
# CUDA
#==

# Pick up some TF dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-command-line-tools-${CUDA/./-} \
    cuda-cublas-${CUDA/./-} \
    cuda-cufft-${CUDA/./-} \
    cuda-curand-${CUDA/./-} \
    cuda-cusolver-${CUDA/./-} \
    cuda-cusparse-${CUDA/./-} \
    curl \
    libcudnn7 \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libzmq3-dev

RUN apt-get update && \
    apt-get install -y --no-install-recommends libnvinfer5=5.1.5-1+cuda${CUDA} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# For CUDA profiling, TensorFlow requires CUPTI.
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Link the libcuda stub to the location where tensorflow is searching for it and reconfigure
# dynamic linker run-time bindings
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1 \
    && echo "/usr/local/cuda/lib64/stubs" > /etc/ld.so.conf.d/z-cuda-stubs.conf \
    && ldconfig

#==
# TensorFlow
#==

ARG TF_PACKAGE=tensorflow-gpu
ARG TF_PACKAGE_VERSION=1.13.1
USER docker:docker
RUN source /home/docker/.virtualenvs/tensorflow/bin/activate \
    && pip --no-cache-dir install --upgrade pip setuptools \
    && pip install ${TF_PACKAGE}${TF_PACKAGE_VERSION:+==${TF_PACKAGE_VERSION}} \
    && pip install tensorflow-probability==0.6.0
USER root

#==
# PyTorch & Torch C++
#==

# TODO

#==
# ROS
#==

# Setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && apt-get install -q -y tzdata && rm -rf /var/lib/apt/lists/*

# Install packages
RUN apt-get update && apt-get install -q -y \
    dirmngr \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# Setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros1-latest.list

# Install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    python-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

# Bootstrap rosdep
RUN rosdep init && rosdep update

# Install ros packages
ENV ROS_DISTRO melodic
RUN apt-get update && apt-get install -y \
    ros-melodic-desktop-full=1.4.1-0* \
    && rm -rf /var/lib/apt/lists/*

# Add .bashrc
USER docker:docker
RUN echo "alias ros_enable=\"source /opt/ros/$ROS_DISTRO/setup.bash\"" >> ~/.bashrc
USER root

#==
# TensorFlow C++
#==

# TODO


#==
# User Configurations
#==

USER docker:docker
COPY ./init.sh /home/docker/.init.sh
WORKDIR /home/docker/
RUN git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install
RUN mkdir git ws

#==
# CLion
#==

# TODO

#==
# Execution
#==

ENTRYPOINT ["/home/docker/.init.sh"]
CMD ["/bin/bash"]

# EOF
