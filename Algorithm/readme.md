#pill_eat - ki_thousand

실행파일이름 : main.py

'''
$ python3 main.py
'''


##pill_eat 기능설명

###class별 기능설명 
Message.py
LCD와 SPEAKER로 사용자에게 알림기능파일
'''
class Message():
- welcome_Pilleat(): 웰컴필잇!!!
- fill_Pill(): 알약을 채워
- eatTime_Pill(): 약을 복용해야하는 시간을 알려주는 기능
- info_Pill(): 약의 이름과 성분 설명해주는 기능
- overlap_Pill(): 중복된 약을 알려주는 기능
- loading_Wait(): 로딩중임을 표시하는기능
- display_Time_now(): 현재시간을 표시해주는기능
'''

led.py
LED와 SENSOR를 제어하는 파일
'''
class led:
- led_on(): LED를 켜는기능 (주로 알약분석시 활용)
- led_off(): LED를 끄는기능 

class sensor:
- sensor_state(): IR SENSOR 감지값을 읽는기능 (TRAY가 있는지 확인할때 사용)
'''


detect_Pill.py
AI모델을 사용하는 파일
'''
class analysis_pill:
- analysis_Pill(): TRAY에 있는 알약을 분석하는기능 (LCD와 SPEAKER출력도 포함되어있음)
'''


