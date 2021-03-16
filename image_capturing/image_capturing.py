import cv2
import numpy as np
import time

def _find_biggest_contour(img, raw):
    max_area = 0
    biggest_contour = np.array([])
    raw = raw.copy()
    contours, hirachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(raw, contours, -1, (0,255,0), 5)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            biggest_contour = contour
    return raw

def _canny_with_cleanup(img):
    canny = cv2.Canny(img, 50, 50)
    kernel = np.ones((3,3))
    dail = cv2.dilate(canny, kernel, iterations = 2)
    return cv2.erode(dail, kernel, iterations = 1)

def get_blackboard_or_none(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 1)
    canny = _canny_with_cleanup(blur)
    edges = _find_biggest_contour(canny, img)
    return edges