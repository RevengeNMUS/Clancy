import cv2
import os
import numpy as nmpy
import pandas
import time
import matplotlib.pyplot as plt
import imutils

face_cascade = cv2.CascadeClassifier(
    "oiter/haarcascade_frontalface_default.xml"
)
smth = cv2.VideoCapture(0)

while True:
    _, frame = smth.read()
    fam = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_rect = face_cascade.detectMultiScale(fam)

    for (x, y, w, h) in face_rect:
        cv2.rectangle(fam, (x, y), (x + w, y + h), (100, 255, 100), 3)

    cv2.imshow("Video Frame", fam)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break


smth.release()
cv2.destroyAllWindows()