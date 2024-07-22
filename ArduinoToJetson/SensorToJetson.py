import sys
import serial
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# PyQt5 DPI 설정
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # DPI 스케일링 활성화
sys.argv += ['--style', 'fusion']

# 시리얼 포트 설정 및 연결
serial_port = '/dev/ttyACM0'  # 시리얼 포트 설정 (적절히 변경)
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 전역 변수 선언 및 초기화
A0_data = []
A1_data = []
A2_data = []

is_reading = True

def read_serial_data(ser):
    global A0_data, A1_data, A2_data, is_reading

    while is_reading:
        if ser.in_waiting > 0:
            raw_data = ser.readline()
            try:
                # 데이터 디코딩 시도
                line = raw_data.decode('utf-8').rstrip()
                if "Colors" in line:
                    # 센서 값만 추출
                    values = line.split(",")
                    A0_value = int(values[0].split(":")[1].strip())
                    A1_value = int(values[1].split(":")[1].strip())
                    A2_value = int(values[2].split(":")[1].strip())
                    A0_data.append(A0_value)
                    A1_data.append(A1_value)
                    A2_data.append(A2_value)

                    print(f"A0 value: {A0_value}, A1 value: {A1_value}, A2 value: {A2_value}")

                    # 각 데이터 리스트의 크기를 50으로 유지
                    for data_list in [A0_data, A1_data, A2_data]:
                        if len(data_list) > 50:
                            data_list.pop(0)
            except UnicodeDecodeError:
                print("디코딩 오류:", raw_data)
            except ValueError:
                print("값 변환 오류:", line)

def update_graph(frame):
    if len(A0_data) > 0:
        x_len = len(A0_data)
        x_data = np.arange(x_len)

        # 그래프 데이터 업데이트
        lines[0].set_data(x_data, A0_data)
        lines[1].set_data(x_data, A1_data)
        lines[2].set_data(x_data, A2_data)

        # 축 범위 조정
        ax.set_xlim(0, max(50, x_len - 1))

    return lines

# 그래프 초기 설정
fig, ax = plt.subplots()
x_data = np.arange(50)
lines = [ax.plot(x_data, np.zeros(50), label=label)[0] for label in ['A0', 'A1', 'A2']]
ax.set_xlim(0, 50)
ax.set_ylim(0, 1023)
ax.legend()

# 시리얼 데이터 읽기를 위한 스레드 시작
thread = threading.Thread(target=read_serial_data, args=(ser,))
thread.start()

# 애니메이션 시작
ani = FuncAnimation(fig, update_graph, blit=False, interval=1)

# 그래프 표시
plt.show()

# 종료 시 처리
is_reading = False
thread.join()
ser.close()



