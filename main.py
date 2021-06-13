import cv2
from camera_calibration.camera import DistortionCamera 
from image_capturing.green_detection import Blackboard
import matplotlib.pyplot as plt
import numpy as np

class Main:
    def __init__(self, use_camera, recalibrate_camera):
        self.buffer = []

        if use_camera:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096.0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160.0)
        else:
            self.cap =cv2.VideoCapture("testfiles/vid1.mp4")

        self.currentCamera: DistortionCamera
        if recalibrate_camera:
            self.currentCamera = DistortionCamera.create_camera_matrix_from_directory("", ".jpg", "CurrentCamera.object")
        else:
            self.currentCamera = DistortionCamera.create_matrix_from_file("CurrentCamera.object")

    def main(self):
        ret, img = self.cap.read()
        if ret:
            img = self.currentCamera.undistort_image(img)
            img = Blackboard.from_image(img)
            if img.contour is not None:
                img = self.validate_corners(img)
            return img

    def validate_corners(self, img):
        corners = Blackboard.sort_points(img.contour)
        in_range = True
        for buf in self.buffer:
            buf_corners = Blackboard.sort_points(buf.contour)
            for i in range(3):
                for j in range(1):
                    if not (buf_corners[i,j] - 10 <= corners[i,j] <= buf_corners[i,j] + 10):
                        in_range = False
                        break
                if not in_range: break
            if not in_range: break

        self.buffer.append(img)
        if len(self.buffer) > 10: self.buffer.pop(0)

        if in_range: return img
        else: return Blackboard(img.image)
                

    def __del__(self):
        self.cap.release()

if __name__ == '__main__':
    values = []
    time = []
    cur_frame = 0
    detection = Main(use_camera=False, recalibrate_camera=False)
    while True:
        cur_frame += 1
        if (img := detection.main()) is not None:
            if img.contour is not None:
                board = img.get_blackboard()
                cv2.imshow("board", board)
                thres = cv2.Canny(board, 100, 200)
                cv2.imshow("thres", thres)
                values.append(np.sum(thres))
                time.append(cur_frame)
            cv2.imshow("frame", img.draw_boundingbox())
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    del detection
    cv2.destroyAllWindows()
    
    plt.plot(time, values)
    plt.show()
