from hacadet_pkg import cv, os, SAVE_PATH


def save_frame(frame, frame_count):
    filename = os.path.join(SAVE_PATH, f"frame_{frame_count}.jpg")
    cv.imwrite(filename, frame)
