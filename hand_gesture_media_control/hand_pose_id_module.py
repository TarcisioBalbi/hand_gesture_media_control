# -*- coding: utf-8 -*-
"""
Created on Sat May 29 13:11:45 2021

@author: Tarcisio Balbi
"""
import cv2
import hand_tracking_module as htm
import numpy as np


class handPoseId():
    def __init__(self):
        self.knownProportions = {'1':[[1.,         2.12251269, 0.51181184, 0.43272611, 0.63624563],
                          [0.4711397,  1.,         0.24113488, 0.20387445, 0.29976058],
                          [1.95384305, 4.14705666, 1.,         0.8454789,  1.2431241 ],
                          [2.31093057, 4.90497946, 1.18276162, 1.,         1.47031947],
                          [1.57172003, 3.33599571, 0.80442492, 0.6801243,  1.        ]],
                    '2':[[1.,         2.286581,   2.29233952, 0.55457735, 0.56329315],
                          [0.43733417, 1.,         1.0025184,  0.24253563, 0.24634734],
                          [0.43623555, 0.99748793, 1.,         0.24192636, 0.2457285 ],
                          [1.80317497, 4.12310563, 4.13348924, 1.,         1.01571611],
                          [1.77527455, 4.05930907, 4.06953202, 0.98452706, 1.        ]],
                    '3':[[1.,         2.26891427, 2.32795599, 2.23391709, 1.08934844],
                          [0.44073944, 1.,         1.02602201, 0.98457536, 0.48011882],
                          [0.42956139, 0.97463796, 1.,         0.95960452, 0.46794203],
                          [0.44764419, 1.01566628, 1.04209596, 1.,         0.4876405 ],
                          [0.91797993, 2.08281775, 2.13701687, 2.05069105, 1.        ]],
                    '4':[[1. ,        2.36392091, 2.42982341, 2.28442263, 2.02600634],
                          [0.423026,   1.,         1.02787847, 0.96637016, 0.85705335],
                          [0.41155254, 0.97287766, 1.,         0.94015994, 0.83380806],
                          [0.43774737, 1.03480016, 1.06364881, 1.,         0.88687895],
                          [0.49358187, 1.16678851, 1.19931679, 1.1275496,  1.        ]],
                    '5':[[1,         1.38460879, 1.41662096, 1.33267218, 1.18263184],
                          [0.72222566, 1.,         1.02312001, 0.96249005, 0.85412707],
                          [0.70590513, 0.97740244, 1.,         0.94074012, 0.83482588],
                          [0.75037208, 1.03897178, 1.06299282, 1.,         0.88741392],
                          [0.84557168, 1.17078599, 1.19785457, 1.12686986, 1.        ]],
                    'thumbsup':[[ 1.,          0.4017531,   0.26449589,  0.10549939,  0.05897595],
                                 [ 2.48909093,  1.,          0.65835431,  0.26259757,  0.1467965 ],
                                 [ 3.78077713,  1.51893894,  1.,          0.39886967,  0.22297493],
                                 [ 9.47872796,  3.80810835,  2.50708456,  1. ,         0.55901699],
                                 [16.95606405,  6.81215131,  4.48480919,  1.78885438,  1.        ]],
                    'hangloose':[[1.,         0.40326468, 0.33290716, 0.37170357, 1.09292716],
                                  [2.47976094, 1.,         0.82553017, 0.921736,   2.71019808],
                                  [3.00384047, 1.21134276, 1.,         1.11653823, 3.28297883],
                                  [2.69031582, 1.08490935, 0.8956254,  1.,         2.94031923],
                                  [0.91497406, 0.36897672, 0.30460142, 0.34009913, 1.        ]]}
        
        
        self.buffer_pos = 0
        self.pose_buffer = ['','','']
        self.currentPose = 'None'
        self.detector = htm.handDetector()
            
    def getHandPose(self,img):
        
            propList = []
            img = self.detector.findHands(img)
            lmList =  self.detector.findPosition(img)
            
            if len(lmList) !=0:
                wrist2tipsDistance = [distanceCalculador(lmList[0][1:3], lmList[i][1:3]) for i in ([4,8,12,16,20])]
                # [thumb,index,middle, ring, pinky]
                prp = proportionCalculator(wrist2tipsDistance)
                propList.append(prp)
                
                propListArray = np.array(propList).reshape(5,5)
                readPose = poseDetection(propListArray,self.knownProportions)
                self.pose_buffer[self.buffer_pos] = readPose
                self.buffer_pos+=1
                if self.buffer_pos>=3:
                    self.buffer_pos = 0
                if 3*self.pose_buffer[0] ==self.pose_buffer[0]+self.pose_buffer[1]+self.pose_buffer[2]:
                    self.currentPose = self.pose_buffer[2]
                    
            return img,self.currentPose
        
        
    

def distanceCalculador(p1,p2):
    squaresSum = 0

    for i in range(len(p1)):
        
      squaresSum += np.power((p2[i]-p1[i]),2)
                             
    return np.sqrt(squaresSum)

def proportionCalculator(points):
    proportions = []
    
    for i,ref_dist in enumerate(points):
        props = points/ref_dist
        
        proportions.append(props)
    
    return proportions

def poseDetection(proportionList,positionDict):
    
    poses = [key for key in positionDict.keys()]
    
    distances = []
    for key,value in positionDict.items():
        d = []
        for i in range(len(proportionList)):
            d.append(distanceCalculador(value[i],proportionList[i]))
        distances.append(np.array(d).mean())
     
    distances =  np.array(distances)
    pose = poses[np.argmin(distances)]
    
    return pose
            
 

def main():
    cap = cv2.VideoCapture(0)
    handPoseIdentifier = handPoseId()
    

    while True:
        propList = []
        sucess,img = cap.read()
        
        img,pose = handPoseIdentifier.getHandPose(img)
        print(pose)
            
        cv2.imshow('Image', img)
        
        key = cv2.waitKey(1)
        if key == 27 or key == 10: ## ESC or ENTER to break
            break
    
    cv2.destroyWindow('Image')
    cap.release() 
    
if __name__=='__main__':
    main()