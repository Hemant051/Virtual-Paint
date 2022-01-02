# Virtual Paint
import cv2
import numpy as np

#seting the frame ratio
frameWidth = 640
frameHeight = 480

#Command to capture video from primary webcam
vid = cv2.VideoCapture(1)
# to set the width of the frame
vid.set(3,640)
# to set the height of the frame
vid.set(4,480)
# to set the brightness of the frame
vid.set(10,150)

myColors = [[5,107,0,19,255,255], #Orange
            [0,65,0,255,0,255], #yellow
            [1,131,52,255,0,255]] # red

myColorValues = [[51,153,255],[0,255,255],[0,0,255]] #

myPoints = []



def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count += 1
        #
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>390:
             cv2.drawContours(imgResult,cnt,-1,(0,255,0),2)
             peri = cv2.arcLength(cnt,True)
             approx = cv2.approxPolyDP(cnt,0.02*peri,True)
             x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

# same loop for reading frames of an video
while True:
    # codee for reading the video
    check,frame = vid.read()
    imgResult = frame.copy()
    newPoints = findColor(frame,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    #showing the frames captured
    cv2.imshow("webcam video", imgResult)
    # conditional statement for stoping the frames display
    if cv2.waitKey(1) & 0XFF == ord("q"):
        break
