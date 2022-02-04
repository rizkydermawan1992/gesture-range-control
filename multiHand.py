import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyfirmata
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)

# port = "COM7"
# board = pyfirmata.Arduino(port)
# servo_pinX = board.get_pin('d:5:s') #pin 5 Arduino
# servo_pinY = board.get_pin('d:6:s') #pin 6 Arduino

posCircle = []
posCircleTarget = []

minHand, maxHand = 20, 220
minDeg, maxDeg = 0, 180
minBar, maxBar = 400, 150
xbox, ybox = 400, 500
wbox, hbox = 450, 450
x_rand = random.randint(xbox + 25, xbox + wbox - 25)
y_rand = random.randint(ybox - hbox + 25, ybox - 25)
score = 0
edgeBox = False

while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw = False)


    if hands:

        hand_l = hands[0]
        lmList_l = hand_l["lmList"]  # List of 21 Landmark points
        length_l, info_l, img = detector.findDistance(lmList_l[8], lmList_l[4], img)


        # Hand 2 (Right)
        if len(hands) == 2:
            hand_r = hands[1]
            lmList_r = hand_r["lmList"]  # List of 21 Landmark points
            length_r, info_r, img = detector.findDistance(lmList_r[8], lmList_r[4], img)  # with draw


            xl = lmList_l[8][0]
            yl = lmList_l[8][1]
            xr = lmList_r[8][0]
            yr = lmList_r[8][1]

            # left x | right y
            circleX = np.interp(length_l, [minHand, maxHand], [xbox+25, xbox+wbox-25])
            circleY = np.interp(length_r, [minHand, maxHand], [ybox-25, ybox-hbox+25])

            servoX = np.interp(length_l, [minHand, maxHand], [minDeg, maxDeg])
            servoY = np.interp(length_r, [minHand, maxHand], [maxDeg, minDeg])

            barX = np.interp(length_l, [minHand, maxHand], [minBar, maxBar])
            barY = np.interp(length_r, [minHand, maxHand], [minBar, maxBar])

            # circle player
            posCircle = [int(circleX), int(circleY)]
            cv2.circle(img, posCircle, 25, (0, 0, 255), cv2.FILLED )

            if xbox+25 < posCircle[0] < xbox+wbox-25 and ybox-hbox+25 < posCircle[1] < hbox+25:
                colBox = [255, 0, 0]
                if edgeBox == False:
                    edgeBox = not edgeBox
            else:
                colBox = [0, 0, 255]
                if edgeBox:
                    score = 0
                    edgeBox = not edgeBox


            # box area
            cv2.rectangle(img, (xbox, ybox+50), (xbox+wbox, ybox-hbox), colBox, 3)
            cv2.rectangle(img, (xbox, ybox), (xbox+wbox, ybox+50), colBox, cv2.FILLED)
            cv2.putText(img, f'Score : {score}', (xbox+80, ybox+40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

            #circle target
            if x_rand-35 < posCircle[0] < x_rand+35 and y_rand-35 < posCircle[1] < y_rand+35   :
                x_rand = random.randint(xbox + 25, xbox + wbox - 25)
                y_rand = random.randint(ybox - hbox + 25, ybox - 25)
                score += 5
            cv2.circle(img, (x_rand, y_rand), 25, (0, 255, 255), cv2.FILLED)

            #bar
            cv2.rectangle(img, (1180, 150), (1215, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (1180, int(barX)), (1215, 400), (0, 255, 0), cv2.FILLED)

            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(barY)), (85, 400), (0, 255, 0), cv2.FILLED)

            #servo control
            # servo_pinX.write(servoX)
            # servo_pinY.write(servoY)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

