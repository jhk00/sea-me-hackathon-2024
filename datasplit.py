import os
import shutil
from sklearn.model_selection import train_test_split

# 원본 이미지 및 레이블 디렉토리
image_dirs = ['green_image', 'red_image']
label_dirs = ['green_label', 'red_label']

# 학습 및 검증 디렉토리
train_image_dir = 'dataset/images/train'
val_image_dir = 'dataset/images/val'
train_label_dir = 'dataset/labels/train'
val_label_dir = 'dataset/labels/val'

# 디렉토리 생성
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# 이미지 파일 리스트와 레이블 파일 리스트
image_files = []
label_files = []

for image_dir, label_dir in zip(image_dirs, label_dirs):
    files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    image_files.extend([os.path.join(image_dir, f) for f in files])
    label_files.extend([os.path.join(label_dir, f.replace('.jpg', '.txt')) for f in files])

# 학습 및 검증 데이터셋으로 분할 (90:10 비율)
train_image_files, val_image_files, train_label_files, val_label_files = train_test_split(
    image_files, label_files, test_size=0.1, random_state=42)

# 파일 이동
for file in train_image_files:
    shutil.move(file, os.path.join(train_image_dir, os.path.basename(file)))

for file in val_image_files:
    shutil.move(file, os.path.join(val_image_dir, os.path.basename(file)))

for file in train_label_files:
    shutil.move(file, os.path.join(train_label_dir, os.path.basename(file)))

for file in val_label_files:
    shutil.move(file, os.path.join(val_label_dir, os.path.basename(file)))

print(f'Training images: {len(train_image_files)}')
print(f'Validation images: {len(val_image_files)}')
print(f'Training labels: {len(train_label_files)}')
print(f'Validation labels: {len(val_label_files)}')
