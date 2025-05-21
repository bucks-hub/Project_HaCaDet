import cv2

def detect_humans(frame, model):
    results = model.predict(frame, conf=0.3, classes=0)
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = map(int, box[:4])
                region = frame[y1:y2, x1:x2]
                frame[y1:y2, x1:x2] = cv2.GaussianBlur(region, (99, 99), 0)
    return frame


def detect_objects(frame, model):
    results = model.predict(frame, conf=0.3)
    #results = model.track(frame, conf=0.3, imgsz=1280)
    cables = []
    skids = []

    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box, cls_id in zip(boxes.xyxy.cpu().numpy(), boxes.cls.cpu().numpy()):
                x1, y1, x2, y2 = map(int, box[:4])
                color = (0, 255, 0) if cls_id == 0 else (255, 0, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                (cables if cls_id == 0 else skids).append((x1, y1, x2, y2))
    return cables, skids, frame


def check_alert(cables, skids, threshold):
    if not cables:
        return None

    lowest_cable = max(c[3] for c in cables)
    for skid in skids:
        skid_top = skid[1]
        if lowest_cable >= skid_top:
            return 'high'
        elif (skid_top - lowest_cable) <= threshold:
            return 'medium'
    return None