import cv2
import numpy as nmpy
import pandas
import time
import matplotlib.pyplot as plt
import imutils

smth = cv2.VideoCapture(0)

_, fram = smth.read()

while True:
    _, frame = smth.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    john = cv2.absdiff(src1=frame, src2=fram)
    _, john = cv2.threshold(john, 50, 100000, cv2.THRESH_BINARY)

    cv2.imshow("Video Frame", john)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    fram = frame

smth.release()
cv2.destroyAllWindows()