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


# rest interface setting
key = os.getenv("maker_key")
event = os.getenv("maker_event_store_sensor")
trigger_url = 'https://maker.ifttt.com/trigger/' + event + '/with/key/' + key

def detect_faces(filename):
    """
    Microsoft Face APIで画像から顔を検出する
    """

    face_image = open(filename, "r+b").read()

    # Miscosoft Face APIへ画像ファイルをPOST
    response = requests.post('https://westus.api.cognitive.microsoft.com/face/v1.0/detect?%s' % face_api_params, data=face_image, headers=face_api_headers)
    results = response.json()

    if response.ok:
        print('Result-->  {}'.format(results))
    else:
        print(response.raise_for_status())
    return results


def shutter_camera():
    """
    ラズパイカメラで撮影する
    """

    # cam.jpgというファイル名、640x480のサイズ、待ち時間5秒で撮影する
    cmd = "raspistill -o cam.jpg -h 640 -w 480 -t 5000"
    subprocess.call(cmd, shell=True)

try:
    while True:
        # 人間センサからデータを読みこむ（0: 検出なし, 1:検出あり）
        human_exists = int(GPIO.input(PIN) == GPIO.HIGH)

        if human_exists:
            print('Human exists!')

            print('Taking a picture in 5 seconds...')
            shutter_camera()
            print('Done.')

            # MS Face APIで顔検出
            print('Sending the image to MS face API...')
            results = detect_faces('cam.jpg')
            print('Done.')

            if len(results) > 0:
                print('Done.')
            else:
                print('No faces detected')
        else:
            print('No human')

        print('Wait 10 seconds...')
        print('------------------')
   
     current = str(datetime.now())
     payload = {'value1':current, 'value2': humanExists, 'value3': smileper}
     r = requests.post(trigger_url, data=payload)
     print("success" if r.status_code == 200 else "fall")
     sleep(10)

except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)

GPIO.cleanup()
