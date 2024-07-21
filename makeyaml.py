import os

# YAML 파일 생성 함수
def create_yaml_file(yaml_path, train_img_dir, val_img_dir, train_label_dir, val_label_dir, class_names):
    yaml_content = f"""
train: {train_img_dir}
val: {val_img_dir}

nc: {len(class_names)}
names: {class_names}
"""
    with open(yaml_path, 'w') as yaml_file:
        yaml_file.write(yaml_content)

# 경로 설정
base_dir = r"C:\Users\sokjh\Desktop\yolov5_traffic\dataset"
train_img_dir = os.path.join(base_dir, "images", "train")
val_img_dir = os.path.join(base_dir, "images", "val")
train_label_dir = os.path.join(base_dir, "labels", "train")
val_label_dir = os.path.join(base_dir, "labels", "val")

# 클래스 이름 설정
class_names = ['Red', 'Green']

# YAML 파일 경로 설정
yaml_path = os.path.join(base_dir, "dataset.yaml")

# YAML 파일 생성
create_yaml_file(yaml_path, train_img_dir, val_img_dir, train_label_dir, val_label_dir, class_names)

print(f"YAML 파일이 생성되었습니다: {yaml_path}")
