# Jetson Nano

Documentation: by Daniel Sanei

### Docker

- Docker containers are ephemeral
    - Changes inside container do not persist after container stops
    - Solution: use volume mounts
        - -v /host/path:/container/path
        - Volume mounts ensure that code files, configurations, and data are saved on the host and remain accessible even after the container is restarted
- Host Directory: directory on host machine that stores ROS2 project files, scripts, and data
- Docker Volume Mount: maps `ros2_humble_workspace` directory from host machine to `/workspace` directory inside Docker container
    - Files in `ros2_humble_workspace` on host are accessible inside Docker container at `/workspace`
    - Changes made inside Docker container in `/workspace` will be reflected in `ros2_humble_workspace` on the host

```bash
# change file ownership
sudo chown -R inspiration:inspiration ~/ros2_humble_workspace
```

### Device Mapping

- Allows specific hardware devices (i.e. cameras, USB devices) on the host to be accessible within the Docker container
- Ensures the container can interact with hardware like it would natively

### Privileged Mode

- Grants the Docker container extended permissions, similar to root access on the host system
- Provides the container with all the capabilities of the host, enabling access to hardware and system resources

### MAVROS

- Package that acts as a bridge between ROS and MAVLink, a communication protocol used by flight controllers like Pixhawk
- Enables control and communication with Pixhawk using ROS topics, services, and actions
- Facilitates integration of drone hardware with ROS-based software for tasks like autonomous flight and sensor data processing

### Docker Containers

- RoboFlow Inference Server Docker (Tin Can) → 9 GB
- ROS2 Humble Docker Container → 13.3 GB

### ROS2 Humble Docker Container

```bash
# pull Docker container
docker pull dustynv/ros:humble-ros-base-l4t-r36.2.0

# with memory (?)
docker run --runtime nvidia -it --network=host dustynv/ros:humble-ros-base-l4t-r36.2.0

# without memory
sudo docker run --runtime nvidia -it --rm --network=host dustynv/ros:humble-ros-base-l4t-r36.2.0

# with ros2 humble workspace
sudo docker run --runtime nvidia -it --network=host -v ~/ros2_humble_workspace:/workspace dustynv/ros:humble-ros-base-l4t-r36.2.0

# with device mapping (Arducam)
sudo docker run --runtime nvidia -it --network=host --privileged -v ~/ros2_humble_workspace:/workspace --device=/dev/video0 dustynv/ros:humble-ros-base-l4t-r36.2.0
--device=/dev/video0

# with device mapping (Pixhawk)
sudo docker run --runtime nvidia -it --network=host --privileged -v ~/ros2_humble_workspace:/workspace --device=/dev/ttyACM0 dustynv/ros:humble-ros-base-l4t-r36.2.0
--device=/dev/ttyACM0

# with device mapping (Arducam and Pixhawk)
sudo docker run --runtime nvidia -it --network=host --privileged -v ~/ros2_humble_workspace:/workspace --device=/dev/video0 --device=/dev/ttyACM0 dustynv/ros:humble-ros-base-l4t-r36.2.0
```

### Install Packages

```bash
# update
sudo apt update

# MAVROS
sudo apt install ros-humble-mavros ros-humble-mavros-extras

# Video4Linux
sudo apt install v4l-utils

# command-line tool to capture images from video devices
sudo apt install fswebcam

# OpenCV
sudo apt install python3-opencv

# source ROS2 environment
source /opt/ros/humble/install/setup.bash
source /opt/ros/humble/setup.bash

# verify MAVROS installation
ros2 pkg list | grep mavros

# verify camera access
v4l2-ctl --list-devices
```

### Inference Docker Container

```bash
# start inference container
sudo docker run --net=host --gpus all roboflow/inference-server:jetson

# start new inference container
sudo docker run --privileged --net=host --runtime=nvidia --mount source=roboflow,target=/tmp/cache -e NUM_WORKERS=1 roboflow/roboflow-inference-server-jetson-4.6.1:latest
```

### Helpful Commands

```bash
# check Arducam connection
ls /dev/video*

# check Pixhawk connection
ls /dev/ttyACM0

# list video devices with details (including names and paths)
v4l2-ctl --list-devices

# remove file
rm -rf [file]

# check Jetpack version
dpkg-query --show nvidia-l4t-core

# check Ubuntu version
lsb_release -a

# copy file to new directory
[sudo] cp ~/[file_to_send] ~/[new_directory]
```

### Cleaning

```bash
# check disk space
df -h

# clears local repository of retrieved package files
sudo apt-get clean

# removes outdated package files from archives
sudo apt-get autoclean

# removes unusued packages
sudp apt-get autoremove
```

### Arducam Live Feed (ROS2)

```bash
# check if Arducam accessible
v4l2-ctl --list-devices

# create ROS2 package for camera node
ros2 pkg create --build-type ament_python my_camera_package
cd my_camera_package

# create camera node script
nano my_camera_package/my_camera_package/camera_node.py

# include new node
nano setup.py

# build package
colcon build
source install/setup.bash

# run camera node
ros2 run my_camera_package camera_node

----------------------------------------------------------------------------------------

# capture Arducam image from ROS2 Humble Docker container
fswebcam -d /dev/video0 /workspace/test_image.jpg
exit
ls ~/ros2_humble_workspace/test_image.jpg
xdg-open ~/ros2_humble_workspace/test_image.j
```

### Arducam Automatic Script

```bash
# line of code to run script upon Jetson Nano startup
nano ~/.bashrc
python3 /path/to/your/arducam_script.py
source ~/.bashrc
```

### YOLO8

```bash
# clone YOLOv8 repository
git clone https://github.com/ultralytics/ultralytics.git

# install dependencies
cd ultralytics
pip install .

# download and unzip dataset
curl -L "https://universe.roboflow.com/ds/95r0htTjlw?key=qkMR7wf9Ff" &gt
roboflow.zip
unzip roboflow.zip
rm roboflow.zip

# curl command to run inference on an image
base64 test_image.jpg | curl -d @- "https://detect.roboflow.com/helipad_detection-2zrua/1?api_key=6BSPzyvwTjTvvM4RkVxd"
```

- Download Dataset
    - RoboFlow Universe → Overview → Download this Dataset → Format = YOLOv8 (show download code) → >_ Terminal → Use curl command
- Inference Command
    - RoboFlow Workspace —> Select Project —> Versions —> Use curl command

### MAVROS

- MAVROS Node
    - Bridges Jetson Nano (ROS2 Humble) to Pixhawk
    - Command needs to stay running to maintain communication
- ROS2 Topics
    - Communication channels in ROS where nodes can publish or subscribe to messages
- Echoing Topics
    - Monitors real-time messages on specified topics

```bash
# attach new terminal to running container
docker ps
docker exec -it <container_id> /bin/bash
[ docker exec -it priceless_ardinghelli /bin/bash ]
source /opt/ros/humble/install/setup.bash

# start MAVROS node to bridge ROS and Pixhawk flight controller
ros2 launch mavros px4.launch fcu_url:=/dev/ttyACM0:57600

# display list of active ROS2 topics currently being published/subscribed in ROS network
ros2 topic list
```

### GitHub

- Personal access token
    1. Settings
    2. Developer settings
    3. Personal access tokens
    4. Tokens (classic)
    5. Generate new token (classic)
    

### Linux Graveyard

```bash
# Docker container for local inference server
sudo docker run --privileged --net=host --runtime=nvidia --mount source=roboflow,target=/tmp/cache -e NUM_WORKERS=1 roboflow/roboflow-inference-server-jetson-4.5.0:latest
	# remove above
	# removed inference Docker image to free up Jetson Nano disk space (from 2 GB to 5.5 GB)

# additional setup for inference
sudo apt update
sudo apt install -y python3-pip v4l-utils fswebcam
pip3 install numpy torch torchvision opencv-python

# install inference
pip3 install inference

# JSON response
inspiration@inspiration:~$ base64 test_image_2.jpg | curl -d @- "http://localhost:9001/helipad_detection-2zrua/2?api_key=6BSPzyvwTjTvvM4RkVxd"
{"time":1.5648549790003017,"image":{"width":640,"height":480},"predictions":[{"x":336.0,"y":169.5,"width":70.0,"height":65.0,"confidence":0.984398603439331,"class":"landing-pads","class_id":1,"detection_id":"f38f6a1f-a3ab-46b7-9408-1d6776ae29ad"},{"x":335.0,"y":171.0,"width":20.0,"height":16.0,"confidence":0.7766841053962708,"class":"circle-target","class_id":0,"detection_id":"7a78373c-df21-40d6-b7d8-96e5550f61cc"}]}inspirabase64 test_image_3.jpg | curl -d @- "http://localhost:9001/helipad_detection-2zrua/2?api_key=6BSPzyvwTjTvvM4RkVxd"
{"time":1.18154845600111,"image":{"width":640,"height":480},"predictions":[{"x":325.0,"y":211.0,"width":58.0,"height":54.0,"confidence":0.9679426550865173,"class":"landing-pads","class_id":1,"detection_id":"a0672df1-39ee-4ffd-be08-e5de9e9637dd"}]}inspiration@inspiration:~$ clear

inspiration@inspiration:~$ base64 test_image_3.jpg | curl -d @- "http://localhost:9001/helipad_detection-2zrua/2?api_key=6BSPzyvwTjTvvM4RkVxd"
{"time":0.31466844500027946,"image":{"width":640,"height":480},"predictions":[{"x":325.0,"y":211.0,"width":58.0,"height":54.0,"confidence":0.9679426550865173,"class":"landing-pads","class_id":1,"detection_id":"ec3a6c6a-c1f3-4ad3-9d21-ee72f3c58dd7"}]}inspiration@inspibase64 test_image_2.jpg | curl -d @- "http://localhost:9001/helipad_detection-2zrua/2?api_key=6BSPzyvwTjTvvM4RkVxd"
{"time":0.37653657000009844,"image":{"width":640,"height":480},"predictions":[{"x":336.0,"y":169.5,"width":70.0,"height":65.0,"confidence":0.984398603439331,"class":"landing-pads","class_id":1,"detection_id":"41e4dec1-b623-4638-b493-d33e5218dd9d"},{"x":335.0,"y":171.0,"width":20.0,"height":16.0,"confidence":0.7766841053962708,"class":"circle-target","class_id":0,"detection_id":"2e140cf0-09f3-48be-83f3-bd56c4a01da2"}]}inspirbase64 test_image.jpeg | curl -d @- "http://localhost:9001/helipad_detection-2zrua/2?api_key=6BSPzyvwTjTvvM4RkVxd"
{"time":18.404477264999514,"image":{"width":1152,"height":1536},"predictions":[]inspiration@inspiration:~$ base64 test_image.jpeg | curl -d @- "http://localhost:9001/helipad_detection-2zrua/2?api_key=6BSPzyvwTjTvvM4RkVxd"
```