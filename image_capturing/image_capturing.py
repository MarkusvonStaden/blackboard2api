import cv2
import numpy as np

def get_blackboard_or_none(img):
    h, w = img.shape[:2]
    scale = 0.5
    h = int(scale*h)
    w = int(scale*w)
    img = cv2.resize(img, (w,h))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    h = cv2.medianBlur(h, 5)
    s = cv2.medianBlur(s, 5)
    v = cv2.medianBlur(v, 5)
    hsv = cv2.merge((h,s,v))

    green_MIN = np.array([45, 25, 25],np.uint8)
    green_MAX = np.array([116, 255, 255],np.uint8)

    green = cv2.inRange(hsv, green_MIN, green_MAX)
    return green


if __name__ == '__main__':
    pass