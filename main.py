import numpy as np
import cv2
from image_capturing.image_capturing import get_blackboard_or_none
import camera_calibration.camera as ca 

camera_changed = True #for developping purpose; will later be set by GUI

if camera_changed == True: 
    CurrentCamera = ca.Camera.calibrate()
    print("CurrentCamera.dist: ")
    print(CurrentCamera.dist)
    print("CurrentCamera.matrix: ")
    print(CurrentCamera.matrix)

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    blackboard = get_blackboard_or_none(frame)

    cv2.imshow('frame',blackboard)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()