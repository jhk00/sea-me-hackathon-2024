import os
import re

def read_and_update_labels(file_path, new_class_id):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        # Strip whitespace characters (including newlines) from the end of each line
        stripped_lines = [line.strip() for line in lines]
        # Remove duplicate lines
        unique_lines = list(set(stripped_lines))
        # Update class id to new_class_id for any starting digits
        updated_lines = [re.sub(r'^\d+', str(new_class_id), line) + '\n' for line in unique_lines]
        return updated_lines
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def write_labels(file_path, labels):
    try:
        with open(file_path, 'w') as file:
            file.writelines(labels)
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")

def process_directory(directory, new_class_id):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                updated_labels = read_and_update_labels(file_path, new_class_id)
                if updated_labels:  # Only write if reading was successful
                    write_labels(file_path, updated_labels)

if __name__ == "__main__":
    base_dir = r"C:\Users\sokjh\Desktop\yolov5_traffic"  # base_dir를 올바르게 변경
    green_dir = os.path.join(base_dir, "green_label")
    red_dir = os.path.join(base_dir, "red_label")
    
    process_directory(green_dir, 1)  # green 폴더의 맨 앞 숫자를 1으로 변경
    process_directory(red_dir, 0)    # red 폴더의 맨 앞 숫자를 0로 변경

