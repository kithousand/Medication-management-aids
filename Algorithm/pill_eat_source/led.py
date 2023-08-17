##########2023-08-14 15:00 엄기천update ##########
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.IN)


class led:
    def led_on(self):
        GPIO.output(17,True)
        
        
    def led_off(self):
        GPIO.output(17,False)
         
class sensor:
    def sensor_state(self):
        input_state = GPIO.input(27)
        #IR SEONSOR 감지
        if input_state == True:
            return True
        #IR SENSOR 미감지
        else:
            return False


 