#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 10:31:02 2021

@author: burakzdd
"""
import rospy
from gorevlendirme1.msg import Hiz_mesafe

def mesajYayini():
    rospy.init_node("publisher_dugumu",anonymous=True)
    pub = rospy.Publisher("Hiz_mesafe_konusu",Hiz_mesafe,queue_size=10)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        hiz = 0.1
        mesafe = 2
        rospy.loginfo("Maksimum Hiz={} Ulaşılacak Mesafe= {}".format(hiz,mesafe))
        pub.publish(hiz,mesafe)
        rate.sleep()
        
mesajYayini()        
     

