from gtts import gTTS
import os

PILL_name = ""
text = ("펜잘 중복이 있습니다 확인해주세요")
tts = gTTS(text, lang='ko')  # 'ko'는 한국어를 나타냅니다.

#tts.save("C:/Users/teee/Desktop/PILL/Voice/penzar_overlap.mp3")  # 음성을 MP3 파일로 저장합니다.
os.system("mpg321 ~/PILL_TEST_0816/Voice/fill_Pill.mp3")  # 저장한 MP3 파일을 재생합니다.
