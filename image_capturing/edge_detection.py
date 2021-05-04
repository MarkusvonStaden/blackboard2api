import cv2
import numpy as np

def _resize(img, scale):
    h, w = img.shape[:2]
    h = int(scale * h)
    w = int(scale * w)
    return cv2.resize(img, (w, h))

def _find_biggest_contour(img, raw):
    max_area = 0
    biggest_contour = np.array([])
    raw = raw.copy()
    contours, hirachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    cv2.drawContours(raw, [c], -1, (0,255,0), 5)
    return raw

def _canny_with_cleanup(img):
    canny = cv2.Canny(img, 50, 50)
    kernel = np.ones((6,6))
    dail = cv2.dilate(canny, kernel, iterations = 2)
    return cv2.erode(dail, kernel, iterations = 1)

def get_blackboard_or_none(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (13,13), 1)
    cv2.imshow("blur", blur)
    canny = _canny_with_cleanup(blur)
    cv2.imshow("canny", canny)
    edges = _find_biggest_contour(canny, img)
    return edges

if __name__ == "__main__":
    cap = cv2.VideoCapture("./testfiles/vid1.mp4")

    while True:
        ret, frame = cap.read()
        frame = _resize(frame, 0.5)

        if ret:
            cv2.imshow("frame", get_blackboard_or_none(frame))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break