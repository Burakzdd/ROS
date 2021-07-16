#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 20:40:57 2021

@author: burakzdd
"""
import rospy
from gorevlendirme1.srv import Goruntu
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class cevapGonder():
    def __init__(self):
         rospy.init_node("server_dugumu")
         rospy.Service("goruntu_kirp",Goruntu,self.kirpmaFonksiyonu)
         self.bridge = CvBridge()
         rospy.Subscriber("camera/rgb/image_raw",Image,self.kameraCallback)
         rospy.spin()
    
    def kameraCallback(self,mesaj):
        img = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
        cv2.imshow("goruntu1",img)
        img2 = img[self.x1:self.x1+self.w1, self.y1:self.y1+self.h1]
        cv2.imshow("goruntu2",img2)
       # cv2.imwrite("goruntu.png",img2)
        cv2.waitKey(1)
       # cv2.destroyAllWindows()
        
    def kirpmaFonksiyonu(self,istek):
        cevap = "Goruntu kirpildi"
        #print(istek.y)
        self.x1= istek.x
        self.y1 = istek.y
        self.w1 = istek.w
        self.h1 = istek.h
        return cevap
        
cevapGonder()        

