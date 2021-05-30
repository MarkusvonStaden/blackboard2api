import cv2
from camera_calibration.camera import DistortionCamera 
from image_capturing.green_detection import Blackboard

camera_changed = False
use_camera = False

if camera_changed: 
    CurrentCamera: DistortionCamera = DistortionCamera.create_camera_matrix_from_directory("", ".jpg", "CurrentCamera.object")
else:
    CurrentCamera: DistortionCamera = DistortionCamera.create_matrix_from_file("CurrentCamera.object")

if use_camera:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096.0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160.0)
else:
    cap = cv2.VideoCapture("testfiles/vid1.mp4")

while(True):
    ret, img = cap.read()
    if ret:
        img = CurrentCamera.undistort_image(img)
        img = Blackboard.from_image(img)
        if img.board is not None:
            cv2.imshow('boundingbox',Blackboard._resize(img.draw_boundingbox(), 0.5))
            cv2.imshow('blackboard', img.board)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()