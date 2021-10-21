import csv
import time

import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)

cap.set(3,1248)
cap.set(4,720)
detector = HandDetector(detectionCon=int(0.8))

class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = data[5]

        self.userAns = None

    def update(self,cursor,bboxes):

        for x,box in enumerate(bboxes):
            x1,y1,x2,y2= box
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns=x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)


pathCSV = 'questions.csv'

with open(pathCSV,newline='\n') as f:
    reader= csv.reader(f)
    data= list(reader)[1:]


qNo= 0
qTotal = len(data)


qList= []

for q in data:
    qList.append(MCQ(q))





det = HandDetector(detectionCon=int(0.8))

while True:
    succ,img = cap.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img,flipType=False)


    if qNo<qTotal:
        mcq = qList[qNo]

        img,bbox = cvzone.putTextRect(img,mcq.question,[100,100],2,2,offset=50,border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2,offset=50,border=5)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2,offset=50,border=5)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2,offset=50,border=5)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2,offset=50,border=5)

        if hands:
           lmlist= hands[0]['lmList']
           cursor = lmlist[8]
           l,info,img=det.findDistance(lmlist[8],lmlist[12],img)

           if l>60:
                mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
                print(mcq.userAns)
                if mcq.userAns is not None:
                    time.sleep(0.8)
                    qNo +=1
    else:
        score=0
        for mcq in qList:
            if mcq.answer == mcq.userAns:
                score+=1
        score = round((score/qTotal) *100,2)
        img, _ = cvzone.putTextRect(img,f'completed', [700, 400], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Score {score}', [1000, 400], 2, 2, offset=50, border=5)

        print(score)

    barValue=150 + (950//qTotal)*qNo
    cv2.rectangle(img,(150,608),(barValue,650),(0,255,0),cv2.FILLED)
    cv2.rectangle(img, (150, 608), (1100, 650), (255, 0, 255), 5)
    img,_=cvzone.putTextRect(img,f'{round(qNo/qTotal *100)}',[400,400],2,2,offset=50,border=5)

    cv2.imshow('img',img)

    cv2.waitKey(1)