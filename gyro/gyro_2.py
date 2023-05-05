from __future__ import print_function
import qwiic_icm20948
import time
import sys
import board
import digitalio
import busio
import math
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_extended_bus import ExtendedI2C as I2C
from madgwick_py.madgwickahrs import * 
from madgwick_py.quaternion import *

#from test_buttons import *

RAD_TO_DEG = 57.2957795
GYRO_SEN_FACTOR = 131

deltat = 0.001 # 1 ms sampling rate
GYRO_MEAS_ERROR = math.pi * (5.0 / 180.0)
beta = math.sqrt(3.0 / 4.0) * GYRO_MEAS_ERROR

IMU = qwiic_icm20948.QwiicIcm20948()
IMU.getAgmt()
accX = IMU.axRaw
accY = IMU.ayRaw
accZ = IMU.azRaw
xRad = np.arctan2(-accY, -accZ)
yRad = np.arctan2(-accX, -accZ)
zRad = np.arctan2(-accY, -accX)

def quaternion_from_euler(roll, pitch, yaw):
  """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion x,y,z,w format
  """
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return qx, qy, qz, qw

SEq_1, SEq_2, SEq_3, SEq_4 = quaternion_from_euler(xRad, yRad, zRad)

def euler_from_quaternion(x, y, z, w):
	"""
	Convert a quaternion into euler angles (roll, pitch, yaw)
	roll is rotation around x in radians (counterclockwise)
	pitch is rotation around y in radians (counterclockwise)
	yaw is rotation around z in radians (counterclockwise)
	"""
	t0 = +2.0 * (w * x + y * z)
	t1 = +1.0 - 2.0 * (x * x + y * y)
	roll_x = math.atan2(t0, t1)

	t2 = +2.0 * (w * y - z * x)
	t2 = +1.0 if t2 > +1.0 else t2
	t2 = -1.0 if t2 < -1.0 else t2
	pitch_y = math.asin(t2)

	t3 = +2.0 * (w * z + x * y)
	t4 = +1.0 - 2.0 * (y * y + z * z)
	yaw_z = math.atan2(t3, t4)

	return roll_x, pitch_y, yaw_z # in radians

def filterUpdate(w_x, w_y, w_z, a_x, a_y, a_z):
    
	global SEq_1, SEq_2, SEq_3, SEq_4

	# Local system variables
	SEqDot_omega_1, SEqDot_omega_2, SEqDot_omega_3, SEqDot_omega_4 = 0.0, 0.0, 0.0, 0.0  # quaternion derivative from gyroscopes elements
	f_1, f_2, f_3 = 0.0, 0.0, 0.0  # objective function elements
	J_11or24, J_12or23, J_13or22, J_14or21, J_32, J_33 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0  # objective function Jacobian elements
	SEqHatDot_1, SEqHatDot_2, SEqHatDot_3, SEqHatDot_4 = 0.0, 0.0, 0.0, 0.0  # estimated direction of the gyroscope error

	# Auxiliary variables  to avoid repeated calculations
	halfSEq_1, halfSEq_2, halfSEq_3, halfSEq_4 = 0.5 * SEq_1, 0.5 * SEq_2, 0.5 * SEq_3, 0.5 * SEq_4
	twoSEq_1, twoSEq_2, twoSEq_3 = 2.0 * SEq_1, 2.0 * SEq_2, 2.0 * SEq_3

	# Normalize the accelerometer measurement
	norm = math.sqrt(a_x * a_x + a_y * a_y + a_z * a_z)
	a_x /= norm
	a_y /= norm
	a_z /= norm

	# Compute the objective function and Jacobian
	f_1 = twoSEq_2 * SEq_4 - twoSEq_1 * SEq_3 - a_x
	f_2 = twoSEq_1 * SEq_2 + twoSEq_3 * SEq_4 - a_y
	f_3 = 1.0 - twoSEq_2 * SEq_2 - twoSEq_3 * SEq_3 - a_z

	J_11or24 = twoSEq_3  # J_11 negated in matrix multiplication
	J_12or23 = 2.0 * SEq_4
	J_13or22 = twoSEq_1  # J_12 negated in matrix multiplication
	J_14or21 = twoSEq_2
	J_32 = 2.0 * J_14or21  # negated in matrix multiplication
	J_33 = 2.0 * J_11or24  # negated in matrix multiplication

	# Compute the gradient (matrix multiplication)
	SEqHatDot_1 = J_14or21 * f_2 - J_11or24 * f_1
	SEqHatDot_2 = J_12or23 * f_1 + J_13or22 * f_2 - J_32 * f_3
	SEqHatDot_3 = J_12or23 * f_2 - J_33 * f_3 - J_13or22 * f_1
	SEqHatDot_4 = J_14or21 * f_1 + J_11or24 * f_2

	# Normalize the gradient
	norm = math.sqrt(SEqHatDot_1 * SEqHatDot_1 + SEqHatDot_2 * SEqHatDot_2 + SEqHatDot_3 * SEqHatDot_3 + SEqHatDot_4 * SEqHatDot_4)
	SEqHatDot_1 /= norm
	SEqHatDot_2 /= norm
	SEqHatDot_3 /= norm
	SEqHatDot_4 /= norm

	# Compute the quaternion derivative measured by gyroscopes
	SEqDot_omega_1 = -halfSEq_2 * w_x - halfSEq_3 * w_y - halfSEq_4 * w_z
	SEqDot_omega_2 = halfSEq_1 * w_x + halfSEq_3 * w_z - halfSEq_4 * w_y
	SEqDot_omega_3 = halfSEq_1 * w_y - halfSEq_2 * w_z + halfSEq_4 * w_x
	SEqDot_omega_4 = halfSEq_1 * w_z + halfSEq_2 * w_y - halfSEq_3 * w_x

	# Compute then integrate the estimated quaternion derivative
	SEq_1 += (SEqDot_omega_1 - (beta * SEqHatDot_1)) * deltat
	SEq_2 += (SEqDot_omega_2 - (beta * SEqHatDot_2)) * deltat
	SEq_3 += (SEqDot_omega_3 - (beta * SEqHatDot_3)) * deltat
	SEq_4 += (SEqDot_omega_4 - (beta * SEqHatDot_4)) * deltat

	# Normalize quaternion
	norm = math.sqrt(SEq_1 * SEq_1 + SEq_2 * SEq_2 + SEq_3 * SEq_3 + SEq_4 * SEq_4)
	SEq_1 /= norm
	SEq_2 /= norm
	SEq_3 /= norm
	SEq_4 /= norm

	return euler_from_quaternion(SEq_1, SEq_2, SEq_3, SEq_4)


def getAngle():
	# B = Button_Matrix(rows, cols)
	
	i2c = I2C(2)
	print("I2C ok!")
	# Create the ADC object using the I2C bus
	ads = ADS.ADS1115(i2c)
	# Create single-ended input on channel 0
	chan = AnalogIn(ads, ADS.P0)

	IMU = qwiic_icm20948.QwiicIcm20948()
	if IMU.connected == False:
		print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	IMU.begin()

	IMU.getAgmt()
	accX = IMU.axRaw
	accY = IMU.ayRaw
	accZ = IMU.azRaw
	xRad = np.arctan2(-accY, -accZ)
	yRad = np.arctan2(-accX, -accZ)
	zRad = np.arctan2(-accY, -accX)

	initQuaternion = Quaternion(quaternion_from_euler(xRad, yRad, zRad))
	angles = MadgwickAHRS(sampleperiod=0.01, quaternion=initQuaternion)

	while True:
		# B.scan_buttons()
		if IMU.dataReady():
			IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables
			accX = IMU.axRaw
			accY = IMU.ayRaw
			accZ = IMU.azRaw
			gyroX = IMU.gxRaw/GYRO_SEN_FACTOR/RAD_TO_DEG
			gyroY = IMU.gyRaw/GYRO_SEN_FACTOR/RAD_TO_DEG
			gyroZ = IMU.gzRaw/GYRO_SEN_FACTOR/RAD_TO_DEG
			# x, y, z = filterUpdate(gyroX, gyroY, gyroZ, accX, accY, accZ)
			angles.update_imu([gyroX, gyroY, gyroZ], [accX, accY, accZ])
			x, y, z = angles.quaternion.to_euler123()
			print(\
			 'x:{: 06f}'.format(RAD_TO_DEG*x)\
			, '\t', 'y:{: 06f}'.format(RAD_TO_DEG*y)\
			, '\t', 'z:{: 06f}'.format(RAD_TO_DEG*z)\
			)
			# xAng = RAD_TO_DEG*(np.arctan2(-accY, -accZ)+math.pi)
			# yAng = RAD_TO_DEG*(np.arctan2(-accX, -accZ)+math.pi)
			# zAng = RAD_TO_DEG*(np.arctan2(-accY, -accX)+math.pi)
			xAng = RAD_TO_DEG*(np.arctan2(-accY, -accZ))
			yAng = RAD_TO_DEG*(np.arctan2(-accX, -accZ))
			zAng = RAD_TO_DEG*(np.arctan2(-accY, -accX))
			# print(\
			# 'accx:{: 06f}'.format(xAng)\
			# , '\t', 'accy:{: 06f}'.format(yAng)\
			# , '\t', 'accz:{: 06f}'.format(zAng)\
			# )

			time.sleep(0.01)
		else:
			print("Waiting for data")
			time.sleep(0.01)
		# time.sleep(0.05)


if __name__ == '__main__':
	try:
		getAngle()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nBye")
		sys.exit(0)

