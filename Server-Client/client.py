#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:10:36 2021
Client düğümü
@author: burakzdd
"""
import rospy
from gorevlendirme1.srv import Goruntu

def istekteBulun(istek_x,istek_y,istek_w,istek_h):
    rospy.wait_for_service("goruntu_kirp")
    try:
        servis = rospy.ServiceProxy("goruntu_kirp",Goruntu)
        donus = servis(istek_x,istek_y,istek_w,istek_h)
        return donus.cevap
    except rospy.ServiceException:
        print("Servisle alakalı hata !!!")

istek_x = int(input("x giriniz: "))
istek_y = int(input("y giriniz: "))
istek_w = int(input("h giriniz: "))
istek_h = int(input("w giriniz: "))

geri_donut = istekteBulun(istek_x,istek_y,istek_w,istek_h)
print(geri_donut)

