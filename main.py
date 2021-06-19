import cv2
from camera_calibration.camera import DistortionCamera 
from image_capturing.green_detection import Blackboard
import numpy as np

class Main:
    def __init__(self, recalibrate_camera = False, path = None):
        self.buffer = []
        self.values = []
        self.boards = []
        self.final_boards = []

        if path is None:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096.0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160.0)
        else:
            self.cap =cv2.VideoCapture(path)

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
        in_range = len(self.buffer)
        for buf in self.buffer:
            buf_corners = Blackboard.sort_points(buf.contour)
            for i in range(4):
                for j in range(2):
                    if not (buf_corners[i,j] - 25 <= corners[i,j] <= buf_corners[i,j] + 25):
                        in_range -= 1
                        break


        self.buffer.append(img)
        if len(self.buffer) > 10: self.buffer.pop(0)

        if in_range > int(len(self.buffer)/2): return img
        else: return Blackboard(img.image)
                

    def __del__(self):
        self.cap.release()


    def loop(self):
        while True:
            if (img := self.main()) is not None:
                if img.contour is not None:
                    self.boards.append(img.get_blackboard())
                    self.values.append(
                        np.sum(
                        cv2.Canny(self.boards[-1], 100, 200)
                        )
                    )

                    self.evaluate_images(160000)

            else: break
        if len(self.boards) > 0: self.final_boards.append(self.boards[-1])

    def save_images(self, directory = ""):
        for index in range(len(self.final_boards)):
            cv2.imwrite(directory + str(index)+".png", self.final_boards[index])


    def evaluate_images(self, threshold):
        if len(self.values) > 20:
            values = [value if value > threshold else 0 for value in self.values]

            if values[-1] == 0 and any(value != 0 for value in values):
                self.final_boards.append(self.boards[self.values.index(max(self.values))])
                self.boards = []
                self.values = []
        

if __name__ == '__main__':
    detection = Main(path="testfiles/test.mp4")
    detection.loop()
    detection.save_images()
    del detection
