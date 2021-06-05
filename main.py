import cv2
from camera_calibration.camera import DistortionCamera 
from image_capturing.green_detection import Blackboard

class Main:
    def __init__(self, use_camera, recalibrate_camera):
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

        self.main()

    def main(self):
        ret, img = self.cap.read()
        if ret:
            img = self.currentCamera.undistort_image(img)
            img = Blackboard.from_image(img)
            print(img)
            return img

    def __del__(self):
        self.cap.release()

if __name__ == '__main__':
    detection = Main(use_camera=False, recalibrate_camera=False)
    while True:
        if (img := detection.main()) is not None:
            if img.board is not None:
                cv2.imshow("board", img.board)
            cv2.imshow("frame", img.draw_boundingbox())
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    del detection