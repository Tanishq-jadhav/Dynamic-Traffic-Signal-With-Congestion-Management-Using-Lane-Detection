import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import ttk

NORM_FONT= ("Verdana", 10)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Message")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

cascade_src = 'cascade/cars.xml'
video_src = 'dataset/cars.mp4'

cap = cv2.VideoCapture(video_src)
car_cascade = cv2.CascadeClassifier(cascade_src)

deltatsum = 0
n = 0
last_time = time.time()

while(1):
    _, frame = cap.read()
    cars = car_cascade.detectMultiScale(frame, 1.1, 1)
    for (x,y,w,h) in cars:
        roi = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    frame = cv2.GaussianBlur(frame,(21,21),0)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_limit = np.array([0,150,150])
    upper_limit = np.array([10,255,255])

    mask = cv2.inRange(hsv, lower_limit, upper_limit)

    kernel = np.ones((3,3),np.uint8)
    kernel_lg = np.ones((15,15),np.uint8)
    
    mask = cv2.erode(mask,kernel,iterations = 1)

    mask = cv2.dilate(mask,kernel_lg,iterations = 1)    
    
    result = cv2.bitwise_and(frame,frame, mask= mask)
    
    thresh = mask
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 1000
    cont_filtered = []    
    
    for cont in contours:
        if cv2.contourArea(cont) > min_area:
            cont_filtered.append(cont)
            print(cv2.contourArea(cont))
    try:
        cnt = cont_filtered[0]
        
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
        
        rows,cols = thresh.shape[:2]
        [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)        
        

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
        print('x= ', cx, '  y= ', cy, ' angle = ', round(rect[2],2))
        if(round(rect[2],2))<-45:
            popupmsg('Lane change detected')
        print(contours)
        print('The Vehicle is changing Lane')
    except:
        print('no Violation')

    cv2.imshow('frame',frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('thresh',thresh)
    #cv2.imshow('im2', im2)
    #cv2.imshow('result', result)
    
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
		
    deltat = time.time() - last_time
    last_time = time.time()    
    deltatsum += deltat
    n += 1
    freq = round(1/(deltatsum/n), 2)
    print('Updating at ' + str(freq) + ' FPS\r', end='')

cap.release()
cv2.destroyAllWindows()