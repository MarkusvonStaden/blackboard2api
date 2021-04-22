import cv2
import numpy as np

def nothing(x):
    pass

def get_blackboard_or_none(img):
    h, w = img.shape[:2]
    scale = 0.4
    h = int(scale*h)
    w = int(scale*w)
    img = cv2.resize(img, (w,h))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    h = cv2.medianBlur(h, 5)
    s = cv2.medianBlur(s, 5)
    v = cv2.medianBlur(v, 5)
    hsv = cv2.merge((h,s,v))

    h_min = cv2.getTrackbarPos('h_min', 'result')
    s_min = cv2.getTrackbarPos('s_min', 'result')
    v_min = cv2.getTrackbarPos('v_min', 'result')

    h_max = cv2.getTrackbarPos('h_max', 'result')
    s_max = cv2.getTrackbarPos('s_max', 'result')
    v_max = cv2.getTrackbarPos('v_max', 'result')

    green_MIN = np.array([h_min, s_min, v_min],np.uint8)
    green_MAX = np.array([h_max, s_max, v_max],np.uint8)

    green = cv2.inRange(hsv, green_MIN, green_MAX)
    return green


if __name__ == '__main__':
    cap = cv2.VideoCapture("./testfiles/vid1.mp4")
    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # cap.set(cv2.CAP_PROP_FPS, 30)


    cv2.namedWindow('result')

    h_min = 50
    s_min = 20
    v_min = 0
    h_max = 100
    s_max = 200
    v_max = 210

    cv2.createTrackbar('h_min', 'result',h_min,179,nothing)
    cv2.createTrackbar('s_min', 'result',s_min,255,nothing)
    cv2.createTrackbar('v_min', 'result',v_min,255,nothing)
    cv2.createTrackbar('h_max', 'result',h_max,179,nothing)
    cv2.createTrackbar('s_max', 'result',s_max,255,nothing)
    cv2.createTrackbar('v_max', 'result',v_max,255,nothing)

    while(True):
        ret, frame = cap.read()
        cv2.imshow("frame", get_blackboard_or_none(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break