import os

# 디렉토리 경로 설정
base_dir = r"C:\Users\sokjh\Desktop\yolov5_traffic\dataset"
image_dir = os.path.join(base_dir, "images")
label_dir = os.path.join(base_dir, "labels")

# 정규화 함수 정의
def normalize_label_file(file_path, img_width, img_height):
    normalized_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            class_id = parts[0]
            x_center = float(parts[1]) / img_width
            y_center = float(parts[2]) / img_height
            width = float(parts[3]) / img_width
            height = float(parts[4]) / img_height
            normalized_line = f"{class_id} {x_center} {y_center} {width} {height}\n"
            normalized_lines.append(normalized_line)
    return normalized_lines

# 이미지 크기 설정 (모든 이미지가 동일한 크기라고 가정)
img_width, img_height = 1280, 720  # 실제 이미지 크기로 대체 필요

# 정규화할 라벨 파일 리스트 생성
label_files = []
for root, dirs, files in os.walk(label_dir):
    for file in files:
        if file.endswith('.txt'):
            label_files.append(os.path.join(root, file))

# 각 라벨 파일에 대해 정규화 수행
for file_path in label_files:
    normalized_lines = normalize_label_file(file_path, img_width, img_height)
    
    # 정규화된 라벨을 파일에 쓰기
    with open(file_path, 'w') as file:
        file.writelines(normalized_lines)

# 정규화 결과 확인을 위해 라벨 파일 내용을 출력
for file_path in label_files:
    with open(file_path, 'r') as file:
        print(f"Contents of {file_path}:")
        print(file.read())
