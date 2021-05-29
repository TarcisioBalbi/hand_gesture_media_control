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

while True:
    propList = []
    sucess,img = cap.read()
    
    img,pose = handPoseIdentifier.getHandPose(img)
    print(pose)
    
    if pose =='hangloose':
        commandFlag =1
        
    if pose == '1' and commandFlag==1:
        keyboard.press(Key.media_play_pause )
        keyboard.release(Key.media_play_pause )
        commandFlag = 0
        
    elif pose == '2' and commandFlag==1:
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.media_volume_up )
        keyboard.release(Key.media_volume_up )
        keyboard.press(Key.media_volume_up )
        keyboard.release(Key.media_volume_up )
        keyboard.press(Key.media_volume_up )        
        keyboard.release(Key.media_volume_up )
        keyboard.release(Key.ctrl_l)
        commandFlag = 0
    elif pose == '3' and commandFlag==1:
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.media_volume_down )
        keyboard.release(Key.media_volume_down )
        keyboard.press(Key.media_volume_down )
        keyboard.release(Key.media_volume_down )
        keyboard.press(Key.media_volume_down )        
        keyboard.release(Key.media_volume_down )
        keyboard.release(Key.ctrl_l)
        commandFlag = 0
    elif pose == '4' and commandFlag==1:
        keyboard.press(Key.ctrl_l)
        keyboard.press(Key.media_next )
        keyboard.release(Key.media_next )
        keyboard.release(Key.ctrl_l)
        commandFlag = 0
        
    cv2.imshow('Image', img)
    
    key = cv2.waitKey(1)
    if key == 27 or key == 10: ## ESC or ENTER to break
        break

cv2.destroyWindow('Image')
cap.release() 