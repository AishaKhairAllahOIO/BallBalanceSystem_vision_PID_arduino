import cv2
import numpy as np

def get_limits(color):

    c=np.uint8([[color]])
    hsv=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit=hsv[0][0][0]-10,100,100
    upperLimit=hsv[0][0][0]+10,255,255

    lowerLimit=np.array(lowerLimit,dtype=np.uint8)
    upperLimit=np.array(upperLimit,dtype=np.uint8)

    return lowerLimit,upperLimit

yellow=[0,255,255]
cap=cv2.VideoCapture(2)

lower_color,upper_color=get_limits(color=yellow)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)

    blurred = cv2.GaussianBlur(mask, (9, 9), 0)

    kernel = np.ones((5,5), np.uint8)
    mask_clean = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)