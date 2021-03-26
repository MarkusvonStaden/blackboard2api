import numpy as np
import cv2
from image_capturing.image_capturing import get_blackboard_or_none

##test comment blabla

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    blackboard = get_blackboard_or_none(frame)

    # Display the resulting frame
    cv2.imshow('frame',blackboard)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()