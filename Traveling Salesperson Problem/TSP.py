#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 13:29:27 2021

@author: burakzdd
"""


#kütüphaneler aktifleştirlir
import numpy as np, random, operator, pandas as pd
import matplotlib.pyplot as plt
import rospy
from  nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2

#başlangıç popülasyonu oluşturulur
def create_starting_population(size,Number_of_city):
    '''Başlangıç popülasyonu oluşturma methodu
    size= şehir(konum) numarası
    Number_of_city= toplamdaki şehir sayısı
    '''
    population = []
    
    for i in range(0,size):
        population.append(create_new_member(Number_of_city))
        
    return population

def pick_mate(N):
    '''rastgele çiftler seçilmektedir
    N= şehir numarasıdır'''
    i=random.randint(0,N)    
    return i


def distance(i,j):
    '''
    Koordinatlar geçildiğinde yöntem iki şehir arasındaki mesafeyi hesaplamaktadır
    i=(x,y) ilk şehrin koordinatları
    j=(x,y) ikinci şehrin koordinatları
    '''
    #i ve j şehirlerinin mesafelerini döndürür
    return np.sqrt((i[0]-j[0])**2 + (i[1]-j[1])**2)

def score_population(population, CityList):  
    '''
    Tüm popülasyonların puanı burada hesaplanmaktadır
    population= Tüm yolları içeren 2 boyutlu dizi
    Citylist= Şehirlerin listesi
    '''
    scores = []
  
    for i in population:
        print(i)
        #yollanan her bir popülasyon için hesaplanan skor değerleri listeye eklenmektedir
        scores.append(fitness(i, CityList))
        #print([fitness(i, the_map)]) 
    return scores

def fitness(route,CityList):
    '''
    Rotaların bireysel uygunluğu burada hesaplanmaktadır
    route= 1 boyutlu dizi (güzergah alınmaktadır)
    CityList = Şehirlerin listesi
    '''
    
    score=0
    #N_=len(route)
    for i in range(1,len(route)):
        k=int(route[i-1])
        l=int(route[i])
        #listedeki iki şehri mesafew fonksiyonuna gönderilerek mesafe hesaplanmaktadır. Skor değerine eklenmektedir.
        score = score + distance(CityList[k],CityList[l])
        
    #Hesaplanan uygunluk döndürülmektedir.    
    return score


def create_new_member(Number_of_city):
    '''
    ;Popülasyonun yeni üyesi oluşturulmaktadır
    '''
    pop=set(np.arange(Number_of_city,dtype=int))
    route=list(random.sample(pop,Number_of_city))
    #oluşturulan rota döndürülür        
    return route


def crossover(a,b):
    '''
    çaprazlama 
    a= rota 1 (route)
    b= rota 2
    oluşturulan çocuk( çaprazlama sonucundaki yeni rota ) döndürülür
    '''
    child=[]
    childA=[]
    childB=[]
    
    
    geneA=int(random.random()* len(a))
    geneB=int(random.random()* len(a))
    
    start_gene=min(geneA,geneB)
    end_gene=max(geneA,geneB)
    
    for i in range(start_gene,end_gene):
        childA.append(a[i])
        
    childB=[item for item in a if item not in childA]
    child=childA+childB
       
    return child


def mutate(route,probablity):
    '''
    mutasyon işlemi yapılır
    route= 1 boyutlu dizi (rota)
    probablity= mutasyon olasılığı
    '''
    #mutasyon işlemi için düğümler karıştırılır
    route=np.array(route)
    for swaping_p in range(len(route)):
        if(random.random() < probablity):
            swapedWith = np.random.randint(0,len(route))
            
            temp1=route[swaping_p]
            
            temp2=route[swapedWith]
            route[swapedWith]=temp1
            route[swaping_p]=temp2
    
    return route
def selection(popRanked, eliteSize):
    selectionResults=[]
    result=[]
    for i in popRanked:
        result.append(i[0])
    for i in range(0,eliteSize):
        selectionResults.append(result[i])
    
    return selectionResults

def rankRoutes(population,City_List):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = fitness(population[i],City_List)
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = False)

def breedPopulation(mating_pool):
    children=[]
    for i in range(len(mating_pool)-1):
            children.append(crossover(mating_pool[i],mating_pool[i+1]))
    return children


def mutatePopulation(children,mutation_rate):
    new_generation=[]
    for i in children:
        muated_child=mutate(i,mutation_rate)
        new_generation.append(muated_child)
    return new_generation

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


def next_generation(City_List,current_population,mutation_rate,elite_size):
    population_rank=rankRoutes(current_population,City_List)
    
    #print(f"population rank : {population_rank}")
    
    selection_result=selection(population_rank,elite_size)
    #print(f"selection results {selection_result}")
    
    mating_pool=matingPool(current_population,selection_result)
    #print(f"mating pool {mating_pool}")
    
    children=breedPopulation(mating_pool)
    #print(f"childern {children}")
    
    next_generation=mutatePopulation(children,mutation_rate)
    #print(f"next_generation {next_generation}")
    return next_generation

def genetic_algorithm(City_List,size_population=1000,elite_size=75,mutation_Rate=0.01,generation=2000):
    '''size_population = popülasyon boyutu (varsayılan olarak 1000 ayaralnır)
        elite_size = Seçilecek en iyi rota sayısı (vaysayılan olarak 75)
        mutation_Rate = Mutasyon oranı olasılığı, [0,1] aralığında olamlı (varsayılan olarak 0.05)
        generation = Nesil sayısı (varsayılan olarak 2000)
        '''
    pop=[]
    progress = []
    
    Number_of_cities=len(City_List)
    #başlangıç popülasyonu oluştururlur
    population=create_starting_population(size_population,Number_of_cities)
    #rank;Routes fonskiyonuna gidlir, orada uygunluk değerlerine göre sıralama yapılarak sürece dahil edilir.
    progress.append(rankRoutes(population,City_List)[0][1])
    print(f"Başlangıç rotası mesafesi {progress[0]}")
    print(f"Başlangıç rotası {population[0]}")
    for i in range(0,generation):
        #Sonraki nesiller oluşturularak sürece eklenir
        pop = next_generation(City_List,population,mutation_Rate,elite_size)
        progress.append(rankRoutes(pop,City_List)[0][1])
    
    
    rank_=rankRoutes(pop,City_List)[0]
    
    
    plt.plot(progress)
    plt.ylabel('Mesafe')
    plt.xlabel('Nesil')
    plt.show()
    print(f"En iyi rota :{pop[rank_[0]]} ")
    print(f"En iyi rotanın mesafesi {rank_[1]}")
    
    return rank_, pop

def newOdom(msg):
    global x
    global y
    global theta
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    msg.pose.pose.position.z = 0
    rot_q = msg.pose.pose.orientation
    
    (roll, pitch, theta) = euler_from_quaternion ([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    
rospy.init_node("Genetik_algoritma_ile_Gezgin_Satıcı")

cityList = []

cityList.append((1,2))
cityList.append((3,1))
cityList.append((2,4))
cityList.append((5,3))
cityList.append((0,1))
    

rank_,pop=genetic_algorithm(City_List=cityList)    
print("\n")
print("\n")
#print(pop[rank_[0]][1])
#print(cityList[pop[rank_[0]][1]])
#print(cityList[0])
cityList.append((0,0))
x = 0.0
y = 0.0
theta = 0.0
pub = rospy.Publisher("/cmd_vel",Twist, queue_size=1)
speed = Twist()
print(cityList[pop[rank_[0]][0]][1])
r = rospy.Rate(4)

for i in range(len(cityList)-1):
    goal = Point ()
    goal.y = cityList[pop[rank_[0]][i]][0]
    goal.x = cityList[pop[rank_[0]][i]][1]
    print("\nHedeflenen konum")
    print(goal)
    while not (abs(goal.x-x)<0.01 and abs(goal.y-y)<0.01):
        rospy.Subscriber("/odom", Odometry, newOdom)
       
        inc_x = goal.x - x
        inc_y = goal.y - y
    
        angle_to_goal = atan2(inc_y, inc_x)
    
        if abs(angle_to_goal - theta) > 0.1:
            speed = Twist()
            speed.linear.x = 0.0
            speed.angular.z = 0.3
            pub.publish(speed)    

        else:
            speed = Twist()
            speed.linear.x = 0.1
            speed.angular.z = 0.0
            pub.publish(speed)    
        r.sleep()    
  #  x = cityList[pop[rank_[0]][i]][1]
   # y = cityList[pop[rank_[0]][i]][0]
    print("Ulaşılan konum")
    print("x="+str(x))
    print("y="+str(y))
print("Başlangıç noktasına dönülüyor")
goal.y = 0
goal.x =0
while not rospy.is_shutdown():
    rospy.Subscriber("/odom", Odometry, newOdom)
       
    inc_x = goal.x - x
    inc_y = goal.y - y
    
    angle_to_goal = atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:
        speed = Twist()
        speed.linear.x = 0.0
        speed.angular.z = 0.3
        pub.publish(speed)    

    else:
        speed = Twist()
        speed.linear.x = 0.1
        speed.angular.z = 0.0
        pub.publish(speed)    
    r.sleep()
    
    