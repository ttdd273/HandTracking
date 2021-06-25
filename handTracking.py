import cv2
import mediapipe as mp
import time

# The number indicates which webcam you're using
cap = cv2.VideoCapture(0)

while True: 
    success, img = cap.read()

    cv2.imshow("Image")
    cv2.waitKey(1)