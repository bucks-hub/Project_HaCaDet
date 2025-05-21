import os

# Model paths
BMW_MODEL_PATH = 'C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/weights/d_train10.pt'
HUMAN_MODEL_PATH = 'C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/weights/yolov8n.pt'

# Camera settings
CAMERA_URL = 'C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/test_files/v1.MOV'
#CAMERA_URL = 'rtsp://root:Axisbacker@10.246.81.121/axis-media/media.amp'
#CAMERA_URL = 'https://root:Axisbacker@10.246.81.121/axis-cgi/media.cgi'
FRAME_SKIP = 18
THRESHOLD = 10  # pixels

# File settings
SAVE_PATH = "C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/anomaly"
os.makedirs(SAVE_PATH, exist_ok=True)

# Sound files
SOUND_PATHS = {
    'high': 'C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/alarm/alarm4.mp3',
    'medium': 'C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/alarm/alarm5.mp3'
}