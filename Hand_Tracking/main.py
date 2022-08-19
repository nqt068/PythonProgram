from ast import While
from gettext import install
import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

height, width = 1280, 720


#Webcam
cap = cv2.VideoCapture(0)
cap.set(3, height)
cap.set(4, width)

#Hand Detector
detector = HandDetector(maxHands = 5, detectionCon = 0.8)

#Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)


while True:
    #Get the frame from the webcam
    success, img = cap.read()
    #Hands
    hands, img = detector.findHands(img)
    #Landmark values - (x,y,z)*21
    data = []
    if hands:
        #get the first hand detected
        hand = hands[0]
        #Get the landmark list
        lmList = hand['lmList']
        # print(lmList)
        for lm in lmList:
            data.extend([lm[0], height-lm[1], lm[2]])
        # print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)


    cv2.imshow("Image", img)
    cv2.waitKey(1)