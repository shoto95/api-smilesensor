# -*- coding: utf-8 -*-
# 接続: I2Cデバイス - Raspberry Pi
#
# temp sensor
# ADT-7410
# VCC - 3.3V
# GND - GND
# SDA - I2C SDA
# SCL - I2C SCL
#
# PRI sensor
# A500BP
import smbus
import RPi.GPIO as GPIO
import requests
import os
from time import sleep
from datetime import datetime

# PRI sensor setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

# temp sensor setup
bus = smbus.SMBus(1)
address_tmp = 0x48
register_tmp = 0x00

# raw data to tmp(c)
def read_tmp_sensor():
    word_data =  bus.read_word_data(address_tmp, register_tmp)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3 # 12ビットデータ
    if data & 0x1000 == 0:  # 温度が正の場合
        temperature = data*0.0625
    else: # 温度が負の場合、絶対値を取ってからマイナスをかける
        temperature = ( (~data&0x1fff) + 1)*-0.0625
    return temperature

# rest interface setting
key = os.getenv("maker_key")
event = os.getenv("maker_event_store_sensor")
trigger_url = 'https://maker.ifttt.com/trigger/' + event + '/with/key/' + key

# ifttt(maker)
def trigger_ifttt():
    # post data
    current = str(datetime.now())
    humanExists = int(GPIO.input(17) == GPIO.HIGH)
    temp = read_tmp_sensor()
    # post
    payload = {'value1': current, 'value2': humanExists, 'value3': temp}
    r = requests.post(trigger_url, data=payload)
    print( "success" if r.status_code == 200 else "fail")
    
try:
    while True:
        trigger_ifttt()
        sleep(10)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
