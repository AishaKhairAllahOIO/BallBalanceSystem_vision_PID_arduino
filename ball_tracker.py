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