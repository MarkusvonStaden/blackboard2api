import cv2
import numpy as np

def _resize(img, scale):
    h, w = img.shape[:2]
    h = int(scale * h)
    w = int(scale * w)
    return cv2.resize(img, (w, h))

def _hough_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (5,5), 1)
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        x1 = int(x0 +1000*(-b))
        x2 = int(x0 -1000*(-b))
        y1 = int(y0 +1000*(a))
        y2 = int(y0 -1000*(a))

        cv2.line(blur, (x1,y1), (x2,y2), (0,0,255), 2)

    return blur

if __name__ == "__main__":
    cap = cv2.VideoCapture("./testfiles/vid1.mp4")

    while True:
        ret, frame = cap.read()
        frame = _resize(frame, 0.4)

        if ret:
            cv2.imshow("frame", _hough_detection(frame))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break