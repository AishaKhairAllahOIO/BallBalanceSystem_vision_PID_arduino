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

    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                cv2.putText(frame, f"X: {int(x)}, Y: {int(y)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Ball Tracking", frame)
    cv2.imshow("Mask", mask_clean)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()            