import cv2
import time
import numpy as np
# Importing the handtracking module
import handTrackingModule as htm
import math

# Pycaw packages
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Parameters
wCam, hCam = 640, 480
pTime = 0

cap = cv2.VideoCapture(1)
# Camera settings
cap.set(3, wCam)
cap.set(4, hCam)

# Creating the handtracking object
detector = htm.handDetector(detectionCon=0.7)

# Code from the pycaw- the audio package
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# print(volume.GetVolumeRange())
# range of the volume is (-96.0, 0.0, 0.125)
volRange = volume.GetVolumeRange()
minVol = -65.0
maxVol = volRange[1]
# volume.SetMasterVolumeLevel(-60.0, None)
vol = 0
volBar = 400

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw= False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        # The landmarks for index and thumb tips are 8,4, respectively

        cv2.line(img, (x1, y1), (x2,y2), (255,0,255), 3)

        # center of the line
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        # Hand range is about 200 to 50
        # Volume range is from minVol to maxVol
        vol = np.interp(length, [50,200], [minVol, maxVol])
        
        volume.SetMasterVolumeLevel(vol, None)
        # print(length, vol)

        # Gives the illusion that you're pressing a button
        if length < 40:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        volBar = np.interp(length, [50, 200], [400, 150])

    # Creating a volume bar
    cv2.rectangle(img, (50,150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50,int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    

    # Calculating fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)),(40,50), cv2.FONT_HERSHEY_COMPLEX,
    1, (255,0,0),2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
