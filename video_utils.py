import cv2
from config import CAMERA_URL

def get_capture():
    return cv2.VideoCapture(CAMERA_URL)

def resize_frame(frame):
    #return cv2.resize(frame, (640, 480))
    return cv2.resize(frame, (1280, 720))