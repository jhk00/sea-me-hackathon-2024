import cv2
import os

# 비디오 파일 경로
video_path = r'C:\Users\sokjh\Desktop\yolov5_traffic\traffic_video\red.mp4'  # 원시 문자열로 변경
# 또는
# video_path = 'C:\\Users\\sokjh\\Desktop\\yolov5_traffic\\traffic_video\\green.mp4'  # 이중 역슬래시로 변경

# 이미지를 저장할 디렉토리 경로
output_dir = r'C:\Users\sokjh\Desktop\yolov5_traffic\red_image'

# 출력 디렉토리가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 비디오의 프레임 레이트 가져오기
fps = cap.get(cv2.CAP_PROP_FPS)
print(f'프레임 레이트: {fps} fps')

# 비디오 길이 가져오기 (프레임 수)
frame_count_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'전체 프레임 수: {frame_count_total}')

# 비디오 길이 (초)
video_length_sec = frame_count_total / fps
print(f'비디오 길이: {video_length_sec:.2f} 초')

# 초당 저장할 프레임 수
desired_frames_per_sec = 24
print(f'초당 저장할 프레임 수: {desired_frames_per_sec:.2f}')

# 저장할 프레임 간격 계산
frame_interval = int(fps / desired_frames_per_sec)
print(f'프레임 간격: {frame_interval}')

frame_count = 0
saved_frame_count = 0
while True:
    # 비디오에서 프레임 읽기
    ret, frame = cap.read()
    
    # 프레임을 제대로 읽었는지 확인
    if not ret:
        break
    
    # 필요한 간격에 해당하는 프레임만 저장
    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_dir, f'frame_{saved_frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1
    
    frame_count += 1

# 비디오 캡처 객체 해제
cap.release()

print(f'{saved_frame_count} frames saved to {output_dir}')


