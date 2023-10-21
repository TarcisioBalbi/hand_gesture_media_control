# -*- coding: utf-8 -*-
"""
Created on Sat May 29 16:24:50 2021

@author: Tarcísio Balbi
"""

import cv2
import hand_tracking_module as htm
import numpy as np
import hand_pose_id_module as hpid
import time
from pynput.keyboard import Key, Controller


keyboard = Controller()

cap = cv2.VideoCapture(0)
handPoseIdentifier = hpid.handPoseId()

commandFlag = 0
# hangloose = command enabeler
# 1 = Play/Pause
# 2 = Volume up
# 3 = Volume down
# 4 = Next track
while True:
    propList = []
    sucess,img = cap.read()
    
    img,pose = handPoseIdentifier.getHandPose(img)
    
    
    if pose =='hangloose':
        if not commandFlag:
            print('Ready for command.')
            commandFlag =1
        
    if pose == '1' and commandFlag==1:
        print('Play/Pause')
        keyboard.press(Key.media_play_pause )
        keyboard.release(Key.media_play_pause )
        commandFlag = 0
        
        
    elif pose == '2' and commandFlag==1:
        print('Volume up')
        while pose=='2':
            keyboard.press(Key.media_volume_up )
            keyboard.release(Key.media_volume_up )
            _,img = cap.read()
            img,pose = handPoseIdentifier.getHandPose(img)
            #cv2.imshow('Image', img)
            #cv2.waitKey(1)
            time.sleep(0.05)
            
        commandFlag = 0
        
    elif pose == '3' and commandFlag==1:
        print('Volume down')
        while pose=='3':
            keyboard.press(Key.media_volume_down )
            keyboard.release(Key.media_volume_down )
            _,img = cap.read()
            img,pose = handPoseIdentifier.getHandPose(img)
            #cv2.imshow('Image', img)
            #cv2.waitKey(1)
            time.sleep(0.2)
        
        commandFlag = 0
        
    elif pose == '4' and commandFlag==1:
        print('Next track')
        keyboard.press(Key.media_next )
        keyboard.release(Key.media_next )
        commandFlag = 0
        
        
    # # cv2.imshow('Image', img)
    cv2.imshow('Esc or Enter to close', np.zeros((200,200)))
    key = cv2.waitKey(1)
    if key == 27 or key == 10: ## ESC or ENTER to break
        break

cv2.destroyAllWindows()
cap.release() 

