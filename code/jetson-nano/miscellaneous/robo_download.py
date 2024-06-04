from roboflow import Roboflow

rf = RoboFlow(api_key="6BSPzyvwTjTvvM4RkVxd")
project = rf.workspace().project("helipad_detection")
version = project.version("zoros")

model_path = version.download("yolov8")
