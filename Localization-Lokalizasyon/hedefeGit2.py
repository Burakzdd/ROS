#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 00:37:52 2021

@author: burakzdd
"""
import rospy
from  nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2

class hedefeGit:
    def __init__(self):
        rospy.init_node("speed_controller")
        self.x = 0.0
        self.y =0.0
        self.theta = 0.0
        rospy.Subscriber("/odom/filtered", Odometry,self.newOdom)
        pub = rospy.Publisher("/cmd_vel",Twist, queue_size=1)
        hiz = Twist()
        r = rospy.Rate(4)
        goal = Point ()
        goal.x = 5
        goal.y = 5
        while not rospy.is_shutdown():
            inc_x = goal.x - self.x
            inc_y = goal.y - self.y
    
            angle_to_goal = atan2(inc_x, inc_y)
            move_forward = False
            if abs(angle_to_goal - self.theta) > 0.1:
                move_forward = True
            hiz.angular.z = angle_to_goal - self.theta 
            if move_forward is True:
                hiz.linear.x = 0.3  
            #    hiz.linear.y = 0.3
            pub.publish(hiz)    
            # sub = rospy.Subscriber("omometry/filtered", Odometry, newOdom)
            r.sleep()    
    def newOdom(self,msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y 
        rot_q = msg.pose.pose.orientation   
        (roll, pitch, self.theta) = euler_from_quaternion(rot_q.x, rot_q.y, rot_q.z, rot_q.w)
        
hedefeGit()        