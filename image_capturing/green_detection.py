import cv2
import numpy as np
from operator import itemgetter

class Frame:
    def __init__(self, image):
        self.image = image
        img = self._resize(image, 0.5)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_blurred = self._blur(hsv)
        mask = self._create_mask(hsv_blurred)
        img_with_contour = self.draw_biggest_contour(mask, img)
        self.contout = img_with_contour

    def _sort_points(self, c):
        points = [c[0,0], c[1,0], c[2,0], c[3,0]]
        sorted_x = sorted(points, key=itemgetter(0))
        sorted_left = sorted_x[:2]
        sorted_right = sorted_x[2:]
        print(np.shape(sorted_left))
        print(sorted_left)
        top_left = sorted_left[0] if sorted_left[0][1] > sorted_left[1][1] else sorted_left[1]
        bottom_left = sorted_left[0] if sorted_left[0][1] < sorted_left[1][1] else sorted_left[1]
        top_right = sorted_right[0] if sorted_left[0][1] > sorted_right[1][1] else sorted_right[1]
        bottom_right = sorted_right[0] if sorted_left[0][1] < sorted_right[1][1] else sorted_right[1]
        return np.float32([top_left, top_right, bottom_left, bottom_right])


    def _resize(self, img, scale):
        h, w = img.shape[:2]
        h = int(scale * h)
        w = int(scale * w)
        return cv2.resize(img, (w, h))


    def _blur(self, img):
        h, s, v = cv2.split(img)
        h = cv2.medianBlur(h, 5)
        s = cv2.medianBlur(s, 5)
        v = cv2.medianBlur(v, 5)
        return cv2.merge((h, s, v))

    def _contour_approx(self, cnt):
        epsilon = 0.025*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        return approx


    def draw_biggest_contour(self, mask, img):
        contours, hirachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)
            c = self._contour_approx(c)

            if len(c) == 4:
                input_points = self._sort_points(c)
                output_points = np.float32([[0, 0],[0, 1500],[500, 0],[500, 1500]])
                mat = cv2.getPerspectiveTransform(input_points, output_points)
                perspective = cv2.warpPerspective(img, mat, (500, 1500))
                perspective = cv2.rotate(perspective, cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imshow("perspective", perspective)

            cv2.drawContours(img, [c], -1, (0, 255, 0), 3)
            x,y,w,h = cv2.boundingRect(c)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            return img


    def _create_mask(self, img):
        h_min = 50
        s_min = 40
        v_min = 0
        h_max = 100
        s_max = 200
        v_max = 255

        green_MIN = np.array([h_min, s_min, v_min], np.uint8)
        green_MAX = np.array([h_max, s_max, v_max], np.uint8)
        mask = cv2.inRange(img, green_MIN, green_MAX)
        kernel = np.ones((15, 15), np.uint8)
        mask_erode = cv2.erode(mask, kernel, iterations=1)
        return cv2.dilate(mask_erode, kernel, iterations=1)

