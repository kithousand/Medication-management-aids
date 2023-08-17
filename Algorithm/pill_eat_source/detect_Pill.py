import torch
import torchvision.transforms as transforms
import onnxruntime
import cv2
import os
from PIL import Image
import Message
from time import *

from flask import Flask, render_template, Response
import threading
from queue import Queue


MESSAGE = Message.Message()

class analysis_pill:
    def analysis_Pill(self):
        # 큐 생성
        frame_queue = Queue()
        # 스레드 종료를 위한 플래그
        thread_exit_flag = False

        app = Flask(__name__)

        def generate_frames():
            while True:
                # 큐에서 프레임 가져오기
                frame = frame_queue.get()

                # 프레임을 바이트 스트림으로 인코딩하여 전송
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                break
                #과부하시 딜레이넣을것
                time.sleep(1)



       
        @app.route('/')
        def index():
            return render_template('index.html')
        @app.route('/video_feed')
        def video_feed():
            return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
        @app.route('/events')
        def events():
            def generate():
                while True:
                    readytosend=send_text
                    sse_message= f"data: {readytosend}\n\n"
                    yield sse_message
                    #time.sleep(1)
        
            return Response(generate(), content_type='text/event-stream')
    
        def start_stream():
            app.run(host='0.0.0.0', port=8000, debug=False)
        
        
        server_thread = threading.Thread(target=start_stream)
        
        
        server_thread.start()
        
        def start_stream():
            app.run(debug=False)
        
    
    

        #이미지 전처리를 위한 변환 정의
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])  
        # ONNX 모델을 ONNX Runtime으로 로드
        ort_session = onnxruntime.InferenceSession('/home/pill/pill_eat/model_ft.onnx') 
        # 클래스 이름 목록
        class_names = ['lopmin', 'nephin', 'penzar_er']

        # 모델을 GPU로 이동 없으면 cpu
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(device)
        print(f"Using device: {device}")
        ort_session.set_providers([f'CUDAExecutionProvider'])
        ort_session.set_providers([f'CPUExecutionProvider'])






        # 결과 저장 배열
        detected_classes = []   
        cap = cv2.VideoCapture(0)  # 웹캠 캡처 객체 생성

        while (True):
            ret, frame = cap.read()

            if not ret:
                break
            
            
            # 프레임을 화면에 보여주기
            #cv2.imshow('Webcam', frame)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, binary_frame = cv2.threshold(gray_frame,150, 255, cv2.THRESH_BINARY)
            # 노이즈 제거를 위한 침식과 팽창 연산
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            eroded_frame = cv2.erode(binary_frame, kernel, iterations=1)
            dilated_frame = cv2.dilate(eroded_frame, kernel, iterations=1)
            #cv2.imshow('Denoised Webcam', dilated_frame)
            # 원본프레임 복사
            contour_frame = frame.copy()
            # 컨투어 찾기
            contours, _ = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # 이미지 리스트 초기화
            roi_images = []
            # 결과 저장 배열 초기화
            detected_classes = []
            count = 0
            for idx, contour in enumerate(contours):
                contour_area = cv2.contourArea(contour)
                if 2000 < contour_area < 55000:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(contour_frame, (x, y), (x + w , y + h ), (0, 255, 0), 2)
                    # cv2.rectangle(contour_frame, (x, y), (x + w + 20, y + h + 20), (0, 255, 0), 2)
                    #roi = frame[y:y + h+20, x:x + w+20]
                    roi = frame[y:y + h, x:x + w]
                    roi_images.append(roi)  # 이미지를 리스트에 추가
                    # 바운딩 박스 근처에 인덱스 번호 출력
                    cv2.putText(contour_frame, str(count), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    count=count+1
            count = 0
            text_y_val = 25
            for idx, roi in enumerate(roi_images):
                #cv2.imshow(f'ROI {idx}', roi)
                # 프레임 전처리
                image = Image.fromarray(roi)
                input_tensor = transform(image)
                input_tensor = input_tensor.unsqueeze(0)  # 배치 차원 추가
                # 추론 수행
                ort_inputs = {ort_session.get_inputs()[0].name: input_tensor.numpy()}
                ort_outs = ort_session.run(None, ort_inputs)
                # 클래스별 확률 계산
                output_probs = torch.softmax(torch.tensor(ort_outs[0]), dim=1)
                # 가장 높은 확률을 가진 클래스 정보 출력
                max_prob = torch.max(output_probs[0])
                max_prob_index = torch.argmax(output_probs[0])
                predicted_class = class_names[max_prob_index]
                # 클래스와 확률 문자열
                text = f'{count}:{predicted_class}: {max_prob:.4f}'  # 클래스와 확률 정보 생성
                # 클래스와 확률 화면에 보이기
                cv2.putText(contour_frame, text, (0, text_y_val), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                text_y_val = text_y_val + 25
                # 클래스 결과 배열에 추가
                detected_classes.append(predicted_class)
                #cv2.imshow("contour_frame",contour_frame)

                #컨투어 프레임 큐에 넣기
                frame_queue.put(contour_frame)

                # 가장 높은 확률의 클래스를 출력
                print(str(count) + " 번째 약")
                count = count + 1
                print(f'Predicted class: {predicted_class} ({max_prob:.4f})')
            print(detected_classes)
            
            #frame_queue.put(contour_frame)
            
            # detected_classes 배열 전체 검사 반복문
            lopminCount=0
            nephinCount=0
            penzar_erCount=0
            for detected_class in detected_classes:
                if detected_class == "Lopmin":
                    lopminCount = lopminCount + 1
                elif detected_class=="nephin":
                    nephinCount=nephinCount+1
                elif detected_class=="penzar_er":
                    penzar_erCount=penzar_erCount+1
            print(f'Predicted lopmin: {lopminCount}')
            print(f'Predicted nephin: {nephinCount}')
            print(f'Predicted penzar_er: {penzar_erCount}')
            if lopminCount>1:
                os.system("mpg321 ~/pill_eat/Voice/Lopmin_overlap.mp3")
                MESSAGE.overlap_Pill("Lopmin")
                send_text ="로프민 중복이 있습니다 확인해주세요 성분:로페라미드 염산염 급성설사에 효과가있습니다"   
            elif nephinCount>1:
                os.system("mpg321 ~/pill_eat/Voice/nephin_overlap.mp3")
                MESSAGE.overlap_Pill("nephin")
                send_text = "네프신 중복이 있습니다 확인해주세요 성분:생약성분  방광염 요도염등에 효과가있습니다"   
            elif penzar_erCount>1:
                os.system("mpg321 ~/pill_eat/Voice/penzar_overlap.mp3")
                MESSAGE.overlap_Pill("penzar")
                send_text = "펜잘 중복이 있습니다 확인해주세요 성분:아세트 아미노펜 해열 감기에인한 통증에 효과가있습니다"  

            if lopminCount == 1:
                MESSAGE.info_Pill("Lopmin")
                send_text ="성분:로페라미드 염산염 급성설사에 효과가있습니다"

            if nephinCount == 1:
                MESSAGE.info_Pill("nephin")
                send_text = "성분:생약성분  방광염 요도염등에 효과가있습니다"
            if penzar_erCount == 1:
                MESSAGE.info_Pill("penzar_er")
                send_text = "성분:아세트 아미노펜 해열 감기에인한 통증에 효과가있습니다"
            frame_queue.put(contour_frame)
            break
            
        sleep(5)
            # 웹캠 해제 및 창 닫기
        cap.release()
        cv2.destroyAllWindows()
        
        
 