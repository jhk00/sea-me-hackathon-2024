import os
from pathlib import Path
import torch

# 모델 로드 (YOLOv5s 모델을 사용)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 이미지 디렉토리 경로 설정
image_dir = Path(r'C:\Users\sokjh\Desktop\yolov5_traffic\red_image')
output_dir = Path(r'C:\Users\sokjh\Desktop\yolov5_traffic\red_label')

# 출력 디렉토리 생성
output_dir.mkdir(parents=True, exist_ok=True)

# 이미지 파일 목록 가져오기
image_files = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png')) + list(image_dir.glob('*.jpeg'))

# 이미지 처리 및 라벨값 저장
for image_file in image_files:
    # 이미지 탐지
    results = model(image_file)

    # 라벨값 저장
    labels = results.pandas().xywh[0]
    label_file = output_dir / f"{image_file.stem}.txt"
    with open(label_file, 'w') as f:
        for index, row in labels.iterrows():
            if row['class'] == 9:  # 9번 클래스만 필터링
                f.write(f"{row['class']} {row['xcenter']} {row['ycenter']} {row['width']} {row['height']}\n")

print(f"Processed {len(image_files)} images and saved labels to {output_dir}")
