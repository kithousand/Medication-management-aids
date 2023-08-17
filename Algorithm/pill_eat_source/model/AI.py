##########2023-08-14 15:00 엄기천update ##########
import torch
import torchvision.transforms as transforms
import onnxruntime
import cv2
import numpy as np
from PIL import Image


# 이미지 전처리를 위한 변환 정의
class analysis_pill():
    def analysis_Pill():
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
        # ONNX 모델을 ONNX Runtime으로 로드
        ort_session = onnxruntime.InferenceSession('model_ft.onnx')
    
        # 클래스 이름 목록
        class_names = ['Elmuco_Tab', 'Gelusam_Tab', 'Lopmin_Cap', 'Tylenol_Powder_160mg']
    
        #사진 전처리
        PILL_path = "captured_Pill_image/captured_image.jpg" 
    
        PILL_Image = cv2.cvtColor(PILL_path, cv2.COLOR_BGR2RGB)
    
        image = Image.fromarray(PILL_Image)
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
    
        # 클래스 이름과 해당 확률을 함께 표시
        for i, class_name in enumerate(class_names):
            prob = output_probs[0][i].item()
            text = f'{class_name}: {prob:.4f}'
    
    
    
    
        # 가장 높은 확률의 클래스를 출력
        print(f'Predicted class: {predicted_class} ({max_prob:.4f})')
    

