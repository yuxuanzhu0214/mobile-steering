from __future__ import print_function
import qwiic_icm20948
import time
import sys
import board
import digitalio
import busio
import math
import numpy as np
from ADC import *
# from IMU import *
from IMU_improved import *
from Kalman import *
from Buttons import Button_Matrix, rows, cols

i2c = I2C(2)
print("I2C ok!")
ADC_in_0, ADC_in_1 = init_ADC()
IMU, angles = init_IMU()
Buttons = Button_Matrix(rows, cols)

uncertainty = 0.05
kf = Kalman(0, uncertainty, 0.1, 1)
avg = []
count = 0
prev_roll = None
roll_list = []
kf_list = []
i = 10 * 70

while i >= 0:
    # Update IMU
    euler_angle = IMU_get_angle(IMU, angles, debug=False)
    # euler_angle2 = IMU_get_angle_2(IMU, angles, debug=False)
    if euler_angle != None:
        roll = round(euler_angle[0], 2)
        pitch = round(euler_angle[1], 0)
        yaw = round(euler_angle[2])
        roll_list.append(roll)
        # if prev_roll != None:
        #     roll_diff = roll - prev_roll
        #     if roll_diff > 179:
        #         roll -= 180
        #     elif roll_diff < -179:
        #         roll += 180
        # prev_roll = roll

        # roll2 = round(euler_angle2[0])
        # pitch2 = round(euler_angle2[1],0)
        # yaw2 = round(euler_angle2[2])
        steering_angle = roll
        # steering_angle = 1 * ((roll) / 120.0 * 32000.0) // 1000 * 1000
        steering_angle = roll // 5 * (32000/(120/5)) // 1000 * 1000
        if roll < 0:
            steering_angle = -1 * (-roll // 5 * (32000/(120/5))) // 1000 * 1000
        # print(f"roll angle {roll}; pitch {pitch}; yaw {yaw};")
        if len(avg) >= 9:
            avg.pop(0)
            avg.append(roll)
            avg_roll = round(avg[0] * 0.1 + avg[1] * 0.1 + avg[2] * 0.1 + avg[3] * 0.1 + avg[4] * 0.1 + avg[5] * 0.1 + avg[6] * 0.1 + avg[7] * 0.1 + avg[8] * 0.2)
            # print(f'roll angle {avg_roll}')
        else:
            avg.append(roll)
            
        if abs(roll - kf.state) < 5:
            uncertainty = 0.01
        else:
            uncertainty = 1
        kf.predict()
        kf.update(roll, uncertainty)
        roll = round(kf.state)
        kf_list.append(kf.state)
        # else:
        #     avg.append(roll)
        # print(f"roll angle {roll}; pitch {pitch}; yaw {yaw}")
        # print(f"roll angle2 {roll2}; pitch2 {pitch2}; yaw2 {yaw2};")
    else:
        print("skip")
    i -= 1
    time.sleep(0.1)

print(roll_list[100:])
print(kf_list[100:])
