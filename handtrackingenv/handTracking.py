import cv2
import mediapipe as mp
import time

# The number indicates which webcam you're using
cap = cv2.VideoCapture(0)

# Landmarking the hand
mpHands = mp.solutions.hands
hands = mpHands.Hands()


while True: 
    success, img = cap.read()

    # Takes in the RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Want to extract information from the results
    results = hands.process(imgRGB)

    #print(results)

    # Runs the webcam
    cv2.imshow("Image", img)
    cv2.waitKey(1)

