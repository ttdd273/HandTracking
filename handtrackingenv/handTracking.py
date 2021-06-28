import cv2
import mediapipe as mp
import time

# The number indicates which webcam you're using
cap = cv2.VideoCapture(1)

# Landmarking the hand
mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

# Calculate the fps
pTime = 0
cTime = 0

while True: 
    success, img = cap.read()

    # Takes in the RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Want to extract information from the results
    results = hands.process(imgRGB)

    #print(results)
    # Drawing the hand
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # 21 ids, numbered 0 to 20
                # Each id contains three coordinate information
                # Have to multiply each value by width and height to get pixels
                # height, width, channel
                h, w, c = img.shape
                # Position of the center
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cycC)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    # Calculate fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # Display fps on the screen
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 
    3,(255,0,0),3)

    # Runs the webcam
    cv2.imshow("Image", img)
    cv2.waitKey(1)

