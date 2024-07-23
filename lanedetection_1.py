import cv2
import os

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 이미지 그레이스케일로 변환

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)  # 이미지 블러 처리

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)  # 이미지 외곽선 검출

image_path = r'C:\Users\sokjh\Desktop\Lane Detection DataSet\image_60\frame_0117.jpg'

# 파일이 존재하는지 확인
if not os.path.isfile(image_path):
    print(f"오류: 파일을 찾을 수 없습니다 - {image_path}")
else:
    origin_img = cv2.imread(image_path)  # 이미지 불러오기
    if origin_img is None:
        print(f"오류: 이미지를 불러올 수 없습니다 - {image_path}")
    else:
        gray_img = grayscale(origin_img)  # 그레이스케일 함수 실행
        blur_img = gaussian_blur(gray_img, 5)  # 블러 함수 실행
        canny_img = canny(blur_img, 50, 200)  # 외곽 검출 함수 실행

        output_path = r'C:\Users\sokjh\Desktop\Lane Detection DataSet\canny_img.jpg'
        cv2.imwrite(output_path, canny_img)  # 이미지 저장
        cv2.imshow('canny', canny_img)  # 이미지 출력
        cv2.waitKey(0)  # 키 입력 전까지 창 띄워놓기
        cv2.destroyAllWindows()  # 모든 cv2 윈도우 끄기
