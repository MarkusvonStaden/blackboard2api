import cv2
import numpy as np

def nothing(x):
    pass


def _resize(img, scale):
    h, w = img.shape[:2]
    h = int(scale * h)
    w = int(scale * w)
    return cv2.resize(img, (w, h))


def _blur(img):
    h, s, v = cv2.split(img)
    h = cv2.medianBlur(h, 5)
    s = cv2.medianBlur(s, 5)
    v = cv2.medianBlur(v, 5)
    return cv2.merge((h, s, v))


def draw_biggest_contour(mask, img):
    contours, hirachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        cv2.drawContours(img, [c], -1, (0, 255, 0), 3)
        x,y,w,h = cv2.boundingRect(c)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        return img


def _create_mask(img):
    if __name__ == "__main__":
        h_min = cv2.getTrackbarPos("h_min", "result")
        s_min = cv2.getTrackbarPos("s_min", "result")
        v_min = cv2.getTrackbarPos("v_min", "result")

        h_max = cv2.getTrackbarPos("h_max", "result")
        s_max = cv2.getTrackbarPos("s_max", "result")
        v_max = cv2.getTrackbarPos("v_max", "result")
        
    else: 
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


def get_blackboard(img):
    # scale down image for faster processing
    img = _resize(img, 0.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_blurred = _blur(hsv)
    mask = _create_mask(hsv_blurred)
    img_with_contour = draw_biggest_contour(mask, img)
    cv2.imshow("mask", mask)

    return img_with_contour


if __name__ == "__main__":
    cap = cv2.VideoCapture("./testfiles/vid1.mp4")
    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # cap.set(cv2.CAP_PROP_FPS, 30)

    cv2.namedWindow("result")

    h_min = 50
    s_min = 40
    v_min = 0
    h_max = 100
    s_max = 200
    v_max = 255

    cv2.createTrackbar("h_min", "result", h_min, 179, nothing)
    cv2.createTrackbar("s_min", "result", s_min, 255, nothing)
    cv2.createTrackbar("v_min", "result", v_min, 255, nothing)
    cv2.createTrackbar("h_max", "result", h_max, 179, nothing)
    cv2.createTrackbar("s_max", "result", s_max, 255, nothing)
    cv2.createTrackbar("v_max", "result", v_max, 255, nothing)

    # frame = cv2.imread("./testfiles/test.png")

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("frame", get_blackboard(frame))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        