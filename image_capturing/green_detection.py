from typing import Optional
from operator import itemgetter
from dataclasses import dataclass
import cv2
import numpy as np

@dataclass
class Blackboard:
    image: np.ndarray
    contour: Optional[np.ndarray] = None
    board: Optional[np.ndarray] = None

    @staticmethod
    def sort_points(c):
        points = c.reshape(4,2)
        rect = np.zeros((4,2), dtype="float32")

        sum = points.sum(axis=1)
        rect[0] = points[np.argmin(sum)]
        rect[2] = points[np.argmax(sum)]

        diff = np.diff(points, axis = 1)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]

        return rect

    @staticmethod
    def _resize(img, scale):
        h, w = img.shape[:2]
        h = int(scale * h)
        w = int(scale * w)
        return cv2.resize(img, (w, h))

    @staticmethod
    def _blur(img, blur):
        h, s, v = cv2.split(img)
        h = cv2.medianBlur(h, blur)
        s = cv2.medianBlur(s, blur)
        v = cv2.medianBlur(v, blur)
        return cv2.merge((h, s, v))

    @classmethod
    def _blackboard_from_contour(cls, img, contour):
        input_points = cls.sort_points(contour)
        output_points = np.float32([[0, 0],[1500, 0],[1500, 500],[0, 500]])
        mat = cv2.getPerspectiveTransform(input_points, output_points)
        return cv2.warpPerspective(img, mat, (1500, 500))

    @staticmethod
    def get_biggest_contour(mask):
        contours, hirachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)
            epsilon = 0.015*cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            if len(approx) == 4:
                return approx*2

    @staticmethod
    def _create_mask(img, h_min = 50, s_min = 40, v_min = 0, h_max = 100, s_max = 200, v_max = 255, kernel_size = (10,10)):
        green_MIN = np.array([h_min, s_min, v_min], np.uint8)
        green_MAX = np.array([h_max, s_max, v_max], np.uint8)
        mask = cv2.inRange(img, green_MIN, green_MAX)
        kernel = np.ones(kernel_size, np.uint8)
        mask_erode = cv2.erode(mask, kernel, iterations=1)
        return cv2.dilate(mask_erode, kernel, iterations=1)


    @classmethod
    def from_image(cls, img):
        low_res = cls._resize(img, 0.5)
        hsv = cv2.cvtColor(low_res, cv2.COLOR_BGR2HSV)
        hsv_blurred = cls._blur(hsv, 5)
        mask = cls._create_mask(hsv_blurred)
        contour = cls.get_biggest_contour(mask)
        return cls(img, contour)


    def draw_boundingbox(self):
        if self.contour is None:
            return self.image
        return cv2.drawContours(self.image, [self.contour], -1, (255,0,0), 2)

    def get_blackboard(self):
        if self.contour is not None:
            self.board = self._blackboard_from_contour(self.image, self.contour)
            return self.board
