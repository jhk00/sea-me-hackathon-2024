#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32MultiArray
import serial
import threading

# 시리얼 포트 설정
serial_port = '/dev/ttyACM0'  # 적절히 변경 필요
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# 글로벌 변수 선언
is_reading = True

def read_serial_data():
    global is_reading
    rospy.init_node('ir_sensor_publisher', anonymous=False)
    pub = rospy.Publisher('/ir_sensor_values', Int32MultiArray, queue_size=10)
    
    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8').rstrip()
            if "Colors" in raw_data:
                values = raw_data.split(" Colors: ")[1].split(",")
                A0_color = int(values[0])
                A1_color = int(values[1])
                A2_color = int(values[2])
                
                msg = Int32MultiArray()
                msg.data = [A0_color, A1_color, A2_color]
                pub.publish(msg)
                rospy.loginfo(f"Published: {msg.data}")
        rate.sleep()

    ser.close()

if __name__ == '__main__':
    try:
        read_serial_data()
    except rospy.ROSInterruptException:
        is_reading = False
        pass
