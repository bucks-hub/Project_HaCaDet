import cv2
import os
from config import SAVE_PATH

def save_frame(frame, frame_count):
    filename = os.path.join(SAVE_PATH, f"frame_{frame_count}.jpg")
    cv2.imwrite(filename, frame)