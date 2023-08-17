##########2023-08-17 11:00 엄기천update ##########
import os
import RPi_I2C_driver 

from time import *
from datetime import datetime

datetime.today().year        
datetime.today().month     
datetime.today().day  
datetime.today().hour        
datetime.today().minute      
datetime.today().second 

mylcd = RPi_I2C_driver.lcd()


class Message:
    def __init__(self):
        print("Message 생성자호출")
    
    def welcome_Pilleat(self):
        mylcd.lcd_display_string_pos("HELLO     ",1,1) 
        mylcd.lcd_display_string_pos("PILL EAT !!!",2,3)
        #speaker.speak(voice_Option,"HELLO PILL EAT")
        os.system("mpg321 ~/pill_eat/Voice/welcome_Pilleat.mp3")
        sleep(3)
        mylcd.lcd_clear()
        #mylcd.backlight(0)
        print("안녕하세요 PILL EAT 입니다.")  
     
       
    def fill_Pill(self):
        #speaker.speak(voice_Option,"알약워을채주세요.")
        mylcd.lcd_display_string_pos("FILL",1,1) 
        mylcd.lcd_display_string_pos("the PILL !!!",2,3)
        os.system("mpg321 ~/pill_eat/Voice/fill_Pill.mp3")
        sleep(3)
        mylcd.lcd_clear()
        #mylcd.backlight(0)
        print("알약을채워주세요.")
        
    def eatTime_Pill(self):
        #speaker.speak(voice_Option,"약을 복용할 시간입니다.")
        mylcd.lcd_display_string_pos("It`s time to",1,1) 
        mylcd.lcd_display_string_pos("take your PILL",2,1) 
        os.system("mpg321 ~/pill_eat/Voice/eatTime_Pill.mp3")
        sleep(3)
        mylcd.lcd_clear()
        #mylcd.backlight(0)
        print("약을 복용할 시간입니다.")
    

    def info_Pill(self,Pill_name):
      
        if Pill_name == "Lopmin":
            os.system("mpg321 ~/pill_eat/Voice/Lopmin.mp3")
        elif Pill_name == "nephin":
            os.system("mpg321 ~/pill_eat/Voice/nephin.mp3")
        else:
            os.system("mpg321 ~/pill_eat/Voice/penzar.mp3")
            
        mylcd.lcd_display_string_pos(Pill_name,1,1) 
        mylcd.lcd_display_string_pos("take your PILL",2,1) 
    
        sleep(5)
        mylcd.lcd_clear()
        #mylcd.backlight(0)
        print(f"복용하실 약은 {Pill_name} 입니다.")
        
    def overlap_Pill(self,Pill_name):  
        mylcd.lcd_display_string_pos("It`s same PILL !!!",1,1) 
        mylcd.lcd_display_string_pos(Pill_name+"!!!",2,5)
        sleep(3)
        mylcd.lcd_clear()
        #mylcd.backlight(0)
        
        
    def loading_Wait(self):
        mylcd.lcd_display_string_pos("Loading...",1,1) 
        mylcd.lcd_display_string_pos("Wait Please...",2,3) 
        #os.system("mpg321 ~/PILL_TEST_0816/Voice/eatTime_Pill.mp3")
        sleep(3)
        mylcd.lcd_clear()
        #mylcd.backlight(0)
        print("로딩중입니다 잠시만 기다려주십시오.")
        
     
    
        
    def display_Time_now(self):
        mylcd.lcd_display_string_pos(datetime.today().strftime("%Y-%m-%d"),1,1)  
        mylcd.lcd_display_string_pos(datetime.today().strftime("%H:%M:%S"),2,5)
        
    def display_Time_morning(self):
        if mylcd.lcd_display_string_pos(datetime.today().strftime("%H:%M:%S")) == "08:00:00":
            return True
            
    def display_Time_afternoon(self):
        if mylcd.lcd_display_string_pos(datetime.today().strftime("%H:%M:%S")) == "13:00:00":
            return True
            
    def display_Time_night(self):
        if mylcd.lcd_display_string_pos(datetime.today().strftime("%H:%M:%S")) == "19:00:00":
            return True
            
                   

    
        




