# UAV Drone Replenishment Project

## Overview
The UAV Drone Replenishment project aims to develop an autonomous drone system capable of performing object detection and manipulation tasks in challenging environments. This project is part of Triton AI, a UC San Diego organization participating in RoboNation's 2024 RobotX Maritime Challenge. This project was conducted under the guidance of Professor Kastner and fellow staff for CSE 145 (Embedded System Design Project) during the Spring 2024 quarter.

<div align="center">
    <img src="images/unnamed.gif" alt="UAV Rep Task" />
</div>


## Team Members
- Alec Digirolamo
- Daniel Sanei
- Carson Rae
- Soumi Chakraborty

## Project Structure
- Hardware: Jetson Nano, Pixhawk, Arducam
- Software: ROS2 Humble, OpenCV, ArduCopter, PyTorch, SITL Simulator
- Ground Control Station: QGroundControl
- Object Detection: YOLOv5, OpenCV

## Repository Organization
- /admin: Administrative documents, including reports, documentation, presentations
- /code: Source code for the project
- /images: Images used throughout the repository

## Codebase Details
### Object Detection
- [/code/object-detection](code/object-detection): Python notebooks with intructions for [curating custom dataset](code/object-detection/build_custom_dataset.ipynb) and for [training a custom YOLOv5 model](code/object-detection/train_custom_yolov5.ipynb).
### Jetson Nano
- [/code/jetson-nano/arducam](code/jetson-nano/arducam): Python scripts to take images and videos using downward-facing mounted Arducam
- [/code/jetson-nano/control](code/jetson-nano/control): Flight control software
- [/code/jetson-nano/miscellaneous](code/jetson-nano/miscellaneous): Other Python scripts and files
- [/code/jetson-nano/ros](code/jetson-nano/ros): Volume mount for ROS2 Humble host machine workspace
- [/code/jetson-nano/terminal](code/jetson-nano/terminal): Useful terminal commands

## Media
The images and videos taken from our Arducam and various drone flight tests can be accessed from the following link:
- [Image and Video Storage](https://drive.google.com/drive/folders/1x5Ip4g3WwqQiWM1Pjkvi5ud1pZbha7pc?usp=sharing)


## Data Collection
For this project we needed to create our own datasets for both object detection aspects of our project: tin can detection and helipad detection. To start, we created a temporary tin can dataset by placing three colored tin cans down around campus and taking photos with an iPhone from a high vantage point. This was an attempt to simulate the conditions that the drone would encounter on its missions using the high vantage point and concrete colored background. However, this dataset was created with a significant oversight: the camera used on the drone is an Arducam, not an iPhone. iPhones take much higher quality photos than the Arducam and are less wide lensed than the fisheye lens of the Arducam. Unfortunately, these factors meant that this dataset could not be used to train the model used on the drone in competition, but it did allow us to test the capabilities of our Yolov5 model in tin can detection and learn how to deploy the model on the drone. 

Next, we learned from our mistakes on the first tin can detection dataset and worked to build a helipad detection model using images from the Arducam. To do this, we set up a python script to take a photo once a second and flew our drone above a makeshift helipad in many conditions. The makeshift helipad was made in lieu of the real one by taping 6 grey posters together and drawing circles onto the landing pad to scale. This dataset allowed us to train a detection model on competition similar conditions and worked on the real helipad once we were able to get it printed. 

Finally, we were able to get our real helipad printed and repeated the data collection procedure, with tin cans on the helipad. At this point, we realized that it made more sense to use OpenCV for tin can detection, so we no longer needed a tin can dataset, but we wanted to similar the noise that the RGB cans would cause in a helipad model. 

## Annotation 
Once dataset collection and curation is completed, the next step is to annotate the dataset on Roboflow. Annotation means **creating ground truths** of where the objects that we are looking to detect are located on the image. We used Roboflow’s smart polygon tool to highlight two objects: the `helipad` and the centered `circle-targets`. We annotated more than 1500 images over several iterations of our dataset in order to curate a diverse dataset for our model to train on. 

<div align="center">
    <img src="images/annotating.gif" alt="Annotating Images">
</div>

# Object Detection
For replicating our object detection for this project, we have created two tutorials to follow along. The first provides an overview of how to build a custom dataset on RoboFlow, and the second covers how to train a YOLOv5 model based on custom objects. Both tutorials are located in the following directory:
- /code/object-detection

## Acknowledgements
- Triton AI
- Team Inspiration Robotics
- University of California, San Diego

## Special Thanks
- Jack Silberman
- Alex Szeto
- Colin Szeto
- Aditya Chandra
- Eesh Vij
