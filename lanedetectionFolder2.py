import cv2
import os
import numpy as np

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def hough(img, h, w):
    lines = cv2.HoughLinesP(img, rho=1, theta=np.pi/180, threshold=50, minLineLength=40, maxLineGap=80)
    line_img = np.zeros((h, w, 3), dtype=np.uint8)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color=[255, 255, 255], thickness=145)
    return line_img

def process_image(image_path, output_path):
    origin_img = cv2.imread(image_path)
    
    if origin_img is None:
        print(f"Error: Unable to read image '{image_path}'")
        return
    
    gray_img = grayscale(origin_img)
    blur_img = gaussian_blur(gray_img, 7)
    canny_img = canny(blur_img, 50, 200)
    
    h, w = canny_img.shape
    hough_img = hough(canny_img, h, w)
    
    cv2.imwrite(output_path, hough_img)

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_image(input_path, output_path)

if __name__ == '__main__':
    input_folder = r'C:\Users\sokjh\Desktop\Lane Detection DataSet\image_60'
    output_folder = r'C:\Users\sokjh\Desktop\Lane Detection DataSet\image_60_results'
    process_folder(input_folder, output_folder)