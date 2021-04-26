import cv2
import glob

videos = glob.glob("./testfiles/calibration/65deg/*.mp4")

for video in videos:
    cap = cv2.VideoCapture(video)
    ret, img = cap.read()
    cv2.imwrite(video+".png", img)
    cap.release()
