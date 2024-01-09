import cv2
import torch
import numpy as np
from tracker import *


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap=cv2.VideoCapture('D:\Car_Opencv-master\dataset\highway.mp4')

count=0
tracker = Tracker()




def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', POINTS)

while True:
    ret,frame=cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(800,600))
    results=model(frame)
    a=results.pandas().xyxy[0]
    print(a)
    for index,rows in results.pandas().xyxy[0].iterrows():
        x=int(rows[0])
        y=int(rows[1])
        x1=int(rows[2])
        y1=int(rows[3])
        b=str(rows['name'])
        cv2.rectangle(frame,(x,y),(x1,y1),(0,0,255),2)
        
    
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(0)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
