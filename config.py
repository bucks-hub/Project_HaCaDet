import os

# Model paths
BMW_MODEL_PATH = 'Path to skid-cable detection weight file'
HUMAN_MODEL_PATH = 'Path to COCO trained yolov8 weight file'

# Camera settings
CAMERA_URL = 'link to access the network camera'
FRAME_SKIP = 18
THRESHOLD = 10  # pixels

# File settings
SAVE_PATH = "Path to folder that saves the frames with low hanging cable detections"
os.makedirs(SAVE_PATH, exist_ok=True)

# Sound files
SOUND_PATHS = {
    'high': 'Path to high alarm file',
    'medium': 'Path to medium alarm file'
}
