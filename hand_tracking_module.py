# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:53:27 2021

@author: Tarcisio Balbi
This part is based on Chapter one of the course: Advanced Computer Vision with Python 
Available at: https://www.youtube.com/watch?v=01sAkU_NvOY&list=WL&ab_channel=freeCodeCamp.org
"""

import cv2
import mediapipe as mp


class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionConf=0.5, trackConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf
        
        self.mpHands= mp.solutions.hands
        self.hands= self.mpHands.Hands(self.mode,
                                       self.maxHands,
                                       self.detectionConf, 
                                       self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img, draw=True):
        
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #Finds all landmarnks in the image and draws then in the image, if requested.
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
                    
        return img
    
    def findPosition(self,img,handNo=0):
        lmList = []
        
        h,w,c = img.shape
        #Finds de position of each landmark in the image
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            
            for id, lm, in enumerate(myHand.landmark):
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                
        return lmList
        

        

def main():
    
    cap = cv2.VideoCapture(0)
    detector = handDetector()

        
    while True:
        
        sucess,img = cap.read()
        
        img = detector.findHands(img)
        lmList =  detector.findPosition(img)
        
        if len(lmList) !=0:
            print(lmList[0])
            
        cv2.imshow('Image', img)
        
        key = cv2.waitKey(1)
        if key == 27 or key == 10: ## ESC or ENTER to break
            break
    
    cv2.destroyWindow('Image')
    cap.release()   
    
if __name__ == '__main__':
    main()
