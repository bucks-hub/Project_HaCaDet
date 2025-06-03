from hacadet_pkg import os
# Model paths
BMW_MODEL_PATH = 'Path to detection weight file'

# Camera settings
CAMERA_URL = ['Link to access the Network camera 1', 'Link to access the Network camera 2',...., 'Link to access the Network camera n']
FRAME_SKIP = 18
THRESHOLD = 10  # pixels

# File settings
SAVE_PATH = "Path to the folder that saves the frame with low hanging cable detections"
os.makedirs(SAVE_PATH, exist_ok=True)

# Sound files
SOUND_PATHS = {
    'high': 'Path to high alarm file',
    'medium': 'Path to medium alarm file'
}
