import cv2
from ultralytics import YOLO
import time
model = YOLO("./best.pt")
def realtime(frame):
    result = model(frame)
    boxes = result[0].boxes.cpu().numpy() 
    for i, box in enumerate(boxes):
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        x1=cords[0]
        y1=cords[1]
        x2=cords[2]
        y2=cords[3]
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
    return frame


