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
- /media: Images and videos of drone tests and results

## Codebase Details
- /code/arducam: Python scripts to take images and videos using downward-facing mounted Arducam
- /code/control: Flight control software
- /code/miscellaneous: Other Python scripts and files
- /code/ros: Volume mount for ROS2 Humble host machine workspace
- /code/terminal: Useful terminal commands

## Acknowledgements
- Triton AI
- University of California, San Diego

## Special Thanks
- Jack Silberman
- Alex Szeto
- Colin Szeto
- Aditya Chandra
- Eesh Vij
