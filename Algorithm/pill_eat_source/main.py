import os
import RPi_I2C_driver 
import Message
import led
import detect_Pill

from flask import Flask, render_template, Response
import threading
from queue import Queue

from time import *
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.IN)

 
LCD = RPi_I2C_driver.lcd()
MESSAGE = Message.Message()
ANAL = detect_Pill.analysis_pill()
LED = led.led()
SENSOR = led.sensor()



if __name__ == '__main__':
    #전원들어가면
    #웰컴보이스
    MESSAGE.welcome_Pilleat() 
    MESSAGE.fill_Pill()
    while(True):
       #현재시간출력
       MESSAGE.display_Time_now()
       sleep(3)
      
       #일정시간되면 
       if MESSAGE.display_Time_morning == True:
       
       MESSAGE.eatTime_Pill()
       MESSAGE.fill_Pill()
    
       while(True):
            #트레이 들어오면   
            if SENSOR.sensor_state() == True:
                LED.led_on()
                MESSAGE.loading_Wait() 
                ANAL.analysis_Pill()
                LED.led_off()
                break   
            else:
                MESSAGE.fill_Pill()
           
        
    LCD.backlight(0)
    LED.led_off()
GPIO.cleanup()
