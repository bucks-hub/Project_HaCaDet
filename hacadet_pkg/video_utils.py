from hacadet_pkg import cv, CAMERA_URL


def get_capture():
    return cv.VideoCapture(CAMERA_URL)


def resize_frame(frame):
    # return cv.resize(frame, (640, 480))
    return cv.resize(frame, (1280, 720))
