import cv2
from image_capturing.image_capturing import get_blackboard_or_none
from camera_calibration.camera import DistortionCamera 

camera_changed = True #for developping purpose; will later be set by GUI

if camera_changed == True: 
    CurrentCamera = DistortionCamera.create_camera_matrix_from_directory("", ".jpg")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096.0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160.0)

while(True):
    ret, img = cap.read()
    if ret:
        img = CurrentCamera.undistort_image(img)
        cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()