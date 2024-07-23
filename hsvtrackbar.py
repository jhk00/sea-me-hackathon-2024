import cv2
import numpy as np

def nothing(x):
    pass

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(r'C:\Users\sokjh\Desktop\Lane Detection DataSet\60.mp4')

# 트랙바 창 생성
cv2.namedWindow('Trackbars')

# 트랙바 생성
cv2.createTrackbar('LH', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('LS', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('LV', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('UH', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('US', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('UV', 'Trackbars', 255, 255, nothing)

while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("비디오를 더 이상 읽을 수 없습니다.")
        break

    # 프레임 크기 조정
    dim = (640, 640)
    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    
    hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

    # 트랙바의 현재 위치값을 가져옴
    lh = cv2.getTrackbarPos('LH', 'Trackbars')
    ls = cv2.getTrackbarPos('LS', 'Trackbars')
    lv = cv2.getTrackbarPos('LV', 'Trackbars')
    uh = cv2.getTrackbarPos('UH', 'Trackbars')
    us = cv2.getTrackbarPos('US', 'Trackbars')
    uv = cv2.getTrackbarPos('UV', 'Trackbars')

    # 트랙바 위치를 이용해 HSV 값 범위 설정
    lower_white = np.array([lh, ls, lv])
    upper_white = np.array([uh, us, uv])

    # HSV 이미지에서 범위 내에 있는 값들을 마스크로 설정
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # 원본 이미지와 마스크를 사용하여 결과 이미지 생성
    result = cv2.bitwise_and(resized_frame, resized_frame, mask=mask)

    # 결과 이미지 출력
    cv2.imshow('Original Frame', resized_frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Detected Lanes', result)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
