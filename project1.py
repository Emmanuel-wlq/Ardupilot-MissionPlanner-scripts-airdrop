'''Author: Emmanuel from CAUC-SIAE email:256288170@qq.com
This is a script for calculating the instant temp to airdrop a fixed point. '''

#####目标设定（点完航点后输入）#####
targetwp_lat = 39.1089163
targetwp_lng = 117.3459175
targetwp_alt = 0


#####预设参数#####

safe_altitude = 25        # 最低投放高度（米）
trigger_radius = 5        # 触发半径（米）
speed_compensation = 1.15 # 速度补偿系数
servo_channel = 8         # 舵机控制通道
servo_release_pwm = 1100

servo_fermer_pwm = 3000-servo_release_pwm

delta_dist = 2                 #水平距离判定参数(米) 数值越小精度越高
delaytemp = 0             #空投时间延时参量（秒）
delta_alt = 10            #高度补正值
#####脚本程序初始化#####
print("___initialize___")
from time import sleep
import sys
import math
import clr
import time

print ("Start script")
#####GPS信息获取#####

print("get information from gps")
satellites = cs.satcount

if satellites < 3:
	print('GPS FAILED. WAIT FOR BETTER GPS')
else:
	print('GPS PASSED.')


#####机载传感器参数输入#####
altitude = cs.alt + delta_alt
groundspeed = cs.groundspeed
lat = cs.lat
lng = cs.lng
alt = altitude
lat1 = targetwp_lat
lng1 = targetwp_lng
alt1 = targetwp_alt 

print(f"target set\nlat:{targetwp_lat}\nlng:{targetwp_lng}\nalt:{targetwp_alt}\n")

##### 计算需要补偿的前置量#####

fall_time = math.sqrt((2 * altitude) / (9.8 * 0.8)) # 计算下落时间（考虑空气阻力简化为0.8系数）

predist = groundspeed * (fall_time+delaytemp) * speed_compensation # 计算需要补偿的前置量


#####水平距离计算#####


delta_lat = lat-lat1
delta_lng = lng-lng1
d_lat = delta_lat*111319
d_lng = delta_lng*111319*math.cos((lat1+lat)/2)
dist = math.sqrt(d_lat*d_lat+d_lng*d_lng)

print("ready to drop")
#####主循环判断#####
while ((predist-dist)*(predist-dist)>delta_dist) :
    #####GPS信息获取#####

    print("get information from gps")
    satellites = cs.satcount

    if satellites < 3:
        print('GPS FAILED. WAIT FOR BETTER GPS')
    else:
        print('GPS PASSED.')


    #####机载传感器参数输入#####
    altitude = cs.alt + delta_alt
    groundspeed = cs.groundspeed
    lat = cs.lat
    lng = cs.lng
    alt = altitude
    Lat1 = targetwp_lat
    Lon1 = targetwp_lng
    alt1 = targetwp_alt 

    print(f"target set\nlat:{targetwp_lat}\nlng:{targetwp_lng}\nalt:{targetwp_alt}\n")

    ##### 计算需要补偿的前置量#####

    fall_time = math.sqrt((2 * altitude) / (9.8 * 0.8)) # 计算下落时间（考虑空气阻力简化为0.8系数）

    predist = groundspeed * fall_time * speed_compensation # 计算需要补偿的前置量

    #####水平距离计算#####

    delta_lat = lat-lat1
    delta_lng = lng-lng1
    d_lat = delta_lat*111319
    d_lng = delta_lng*111319*math.cos((lat1+lat)/2)
    dist = math.sqrt(d_lat*d_lat+d_lng*d_lng)
    
    #####计算频率#####
    Script.Sleep(1000)
    print("search for target now")  



#####空投执行程序#####
print("airdrop!!!")
Script.SendRC(servo_channel,servo_release_pwm, True)
Script.Sleep(8000)
Script.SendRC(servo_channel,servo_fermer_pwm, True)
Script.Sleep(8000)
print("mission over")

