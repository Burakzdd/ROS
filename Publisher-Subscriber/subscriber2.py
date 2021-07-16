#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 17:25:34 2021

@author: burakzdd
"""
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from gorevlendirme1.msg import Hiz_mesafe

class mesajDinle():
    def __init__(self):
        rospy.init_node("subscriber_dugumu")
        rospy.Subscriber("Hiz_mesafe_konusu", Hiz_mesafe,self.hiz_mesafe_fonksiyonu)
        rospy.spin()

    def hiz_mesafe_fonksiyonu(self,mesaj):
        rospy.loginfo("Robot maksimum hizi: %lf"%mesaj.v)
        rospy.loginfo("Robot gidilecek mesafe: %lf"%mesaj.x)
        self.varis_noktası=mesaj.x
        rate = rospy.Rate(1)
        pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)
        hiz_mesaji = Twist()
        baslangic = 0.05 
        self.kontrol = True
        while not rospy.is_shutdown():
            rospy.Subscriber("odom",Odometry,self.odomCallback)
            
            if self.kontrol:
                if mesaj.v >= baslangic:
                    hiz_mesaji.linear.x = baslangic
                    pub.publish(hiz_mesaji)
                    baslangic = baslangic + 0.01
                else:
                    hiz_mesaji.linear.x = mesaj.v
                    pub.publish(hiz_mesaji)
            else:
                hiz_mesaji.linear.x = 0
                pub.publish(hiz_mesaji)
                rospy.loginfo("Tebrikler basariyle ulastiniz")
            rospy.loginfo("Robot anlik hizi: %lf"%hiz_mesaji.linear.x)
            rospy.loginfo("Robot guncel mesafe: %lf"%self.guncel_konum)    

            rate.sleep()
        
            
    def odomCallback(self,bilgi):
        self.guncel_konum = bilgi.pose.pose.position.x
        if self.guncel_konum < self.varis_noktası:
            self.kontrol = True
        else:
            self.kontrol = False
    
mesajDinle()    


