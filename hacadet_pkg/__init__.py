# __init__.py

# Define the __all__ variable
__all__ = ['YOLO', 'cv', 'os', 'pg',
           'BMW_MODEL_PATH', 'CAMERA_URL', 'FRAME_SKIP', 'THRESHOLD', 'SAVE_PATH', 'SOUND_PATHS',
           'detect_objects', 'check_alert', 'save_frame', 'SoundManager', 'get_capture', 'resize_frame'
           ]


# Import the submodules
from ultralytics import YOLO
import os
import cv2 as cv
import pygame as pg
from .config import BMW_MODEL_PATH, CAMERA_URL, FRAME_SKIP, THRESHOLD, SAVE_PATH, SOUND_PATHS
from .detector import detect_objects, check_alert
from .file_utils import save_frame
from .sound_manager import SoundManager
from .video_utils import get_capture, resize_frame

print("\nProject HaCaDet: No more low hanging cables!!!")
