import os
from ultralytics import YOLO
import cv2 as cv
import pygame
import keyboard

pygame.mixer.init()
highalert = pygame.mixer.Sound('C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/alarm/alarm3.mp3')
mediumalert = pygame.mixer.Sound('C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/alarm/alarm4.mp3')

# Load the YOLOv8 model
bmw_model = YOLO('C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/weights/d_train10.pt')
human_model = YOLO('C:/Users/qxz60kx/Desktop/projects/HaCaDet/HaCaDet/weights/yolov8n.pt')

# Path to the axis camera link
camera_url = 'https://root:Axisbacker@10.246.81.121/axis-cgi/media.cgi'
capture = cv.VideoCapture(camera_url)   # Create a VideoCapture object

# Frame skipping parameter (e.g., process every 30th frame)
frame_skip = 12
frame_count = 0
save_path = "C:/ultralytics/frame_with_issues"
os.makedirs(save_path, exist_ok=True)
os.chdir(save_path)

while True:
    while capture.isOpened(): 
        isTrue, frame = capture.read()
        if not isTrue:
            print("Failed to read frame. Reconnecting...")
            capture = cv.VideoCapture(camera_url)
            continue
        frame = cv.resize(frame, (640, 480))
        # Skip frames to reduce processing load
        if frame_count % frame_skip == 0:
            
            #Perform human detection on the frame
            human_results = human_model.predict(frame, imgsz=640, conf=0.3, classes=0)
            for human_result in human_results:
                human_boxes = human_result.boxes    # Assuming human_result.boxes contains the detected boxes
                
                if human_boxes is not None:
                    human_xyxy = human_boxes.xyxy.cpu().numpy()
                    
                    for human in human_xyxy:
                        fx_min, fy_min, fx_max, fy_max = int(human[0]), int(human[1]), int(human[2]), int(human[3])
                        human_region = frame[fy_min:fy_max, fx_min:fx_max]
                        human_region_blurred = cv.GaussianBlur(human_region, (99, 99), 0)
                        frame[fy_min:fy_max, fx_min:fx_max] = human_region_blurred


            # Perform object detection on the frame for cables and skids.
            bmw_results = bmw_model.predict(frame, imgsz=640, conf=0.3)
            # Access the bounding box coordinates and class labels
            for bmw_result in bmw_results:
                bmw_boxes = bmw_result.boxes   #Assuming bmw_result.boxes contains the detected boxes
                
                if bmw_boxes is not None:
                    
                    name="frame_%d.jpg" %frame_count
                    
                    bmw_coordinates = bmw_boxes.xyxy.cpu().numpy()  #Convert tensor to numpy array
                    bmw_class_ids = bmw_boxes.cls.cpu().numpy()  #Assuming bmw_class_ids.boxes.cls contains the class labels

                    #Check the shape of xyxy and class_ids
                    print(f'xyxy shape: {bmw_coordinates.shape}')
                    print(f'class_ids shape: {bmw_class_ids.shape}')

                    #Dictionaries to store coordinates by class
                    skid_boxes = []
                    cable_boxes = []
                    

                    for bmw_box, bmw_class_id in zip(bmw_coordinates, bmw_class_ids):
                        x_min, y_min, x_max, y_max = int(bmw_box[0]), int(bmw_box[1]), int(bmw_box[2]), int(bmw_box[3])
                        print(f"Class ID: {bmw_class_id}, Bounding Box: {bmw_box}")
                        if bmw_class_id == 1:
                            skid_boxes.append((x_min, y_min, x_max, y_max))
                            cv.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
                            
                        elif bmw_class_id == 0:
                            cable_boxes.append((x_min, y_min, x_max, y_max))
                            cv.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                            

                    #Check the alarm condition for the lowest cable
                    cv.imshow("output", frame)
                    alert_trigger = False
                    threshold = 50 # 1 cm = 37.8 pixel, 2 cm = 75.6 pixel
                    #Note: This is measured on top of the frame, not on the real scenario.
                    if cable_boxes:  # Check if there are any cables detected
                        lowest_cable_y_lower = max(bmw_box[3] for bmw_box in cable_boxes)  # Find the lowest y_max among cables
                        for skid_box in skid_boxes:
                            skid_y_upper = skid_box[1]
                            print(f'Comparing lowest_cable_y_max={lowest_cable_y_lower} with skid_y_min={skid_y_upper}')
                            if lowest_cable_y_lower >= skid_y_upper:
                                cv.imwrite(name, frame)
                                alert_trigger = True
                                print("High Alert!!! Cable Hanging Low!!!")
                                highalert.play()
                                print('Fix the error and then press <<s>> to continue after stopping alarm')
                                if cv.waitKey(0) & 0xFF == ord('s'):
                                    highalert.stop() 
                            elif (skid_y_upper - lowest_cable_y_lower) <= threshold & lowest_cable_y_lower < skid_y_upper:
                                cv.imwrite(name, frame)
                                alert_trigger = True
                                print("Medium Alert!!! Attention Needed!!!")
                                mediumalert.play()
                                print('Check is everything OK and then press <<s>> to continue after stopping alarm')
                                if cv.waitKey(0) & 0xFF == ord('s'):
                                    mediumalert.stop() 
                            else:
                                print("No Problems")
                        if alert_trigger:
                            break
                else:
                    print('No bounding boxes detected.')

        # Increment frame count
        frame_count += 1

        # Press <<p>> to pause.
        if cv.waitKey(20) & 0xFF == ord('p'):
            break

    print('Press <<c>> to continue the program or <<t>> to terminate the Program')
    if keyboard.read_key() == 'c':
        capture = cv.VideoCapture(camera_url)
        continue
    elif keyboard.read_key() == 't':
        print('Program terminated!!!')
        break

capture.release()
cv.destroyAllWindows()

# Release the VideoCapture object and close all OpenCV windows