#!/usr/bin/env python
# -*- coding:utf-8 -*-

#################################################################
#V1.0  2016-12-29                                               #
#手机连接WIFI自动开灯                                           #
#手机连接WIFI自动播放歌曲                                       #
#V2.0  2017-02-07                                               #
#增加记录手机上线离线的日期和时间文件record.txt                 #
#修改当手机一直在线时，到了开灯的时间点(如到了17:45)不开灯问题  #
#V3.0  2017-10-21                                               #
#增加通过配置文件"phone.conf"配置开灯时间点、IP、播放歌曲等     #
#                                                               #
#                                                               #
#################################################################

import RPi.GPIO as GPIO  
import os
import time

PIN_ID = 12
GPIO.cleanup()
# BOARD编号方式，基于插座引脚编号  
GPIO.setmode(GPIO.BOARD)  
# 输出模式  
GPIO.setup(PIN_ID, GPIO.OUT)  

global status


# 检测手机是否连接路由器
def ping_phone(ip):
    phone_status = os.system('ping -c 4 %s'%(ip))
    return phone_status
# 读取配置文件
def readfile():
    fo = open('/home/pi/src/phone.conf')
    content = fo.readlines()
    fo.close()
    return content

def logfunc(status,led_status,start_time):

    print '000000000000'
    print 'status=',status
    print 'led_sstatus',led_status
    print 'start_time=',start_time
    print 'now_time',t
    print '000000000000'

config_file=readfile()            
status = 0
led_status = 0
start_time = config_file[0]
ip=config_file[1]
while 1:
    t=time.strftime('%H:%M',time.localtime(time.time()))
    Day_time=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    phone = ping_phone(ip)
    txt_file = open('/home/pi/src/record.txt','a')
    #print 'start_time=',start_time
    if phone == 0:
        if status == 0 or led_status == 0:
            if start_time < t:
                led_status = 1
                GPIO.output(PIN_ID, GPIO.HIGH)  # 设置IO高电平
            if status == 0:
                #txt_file = open('/home/pi/src/record.txt','a')
                txt_file.write(Day_time+'_'+t+'        ')
                txt_file.close()
                os.system('mplayer %s'%(config_file[2]))
            status = 1
            #logfunc(status,led_status,start_time)  # debug

    elif phone != 0 and status == 1:
        status = 0
        led_status = 0
        GPIO.output(PIN_ID, GPIO.LOW)  # 设置IO低电平
        #txt_file = open('/home/pi/src/record.txt','a')
        txt_file.write(Day_time+'_'+t+'\n')
        txt_file.close()
        #os.system('mplayer /home/pi/Music/Beautiful_World.mp3')
        os.system('mplayer %s'%(config_file[3]))
        #print 'phone off_line'
    
    if status == 1:
        time.sleep(2*60)     # 手机在线时休眠2分钟
    time.sleep(30)

