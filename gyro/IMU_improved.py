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

"""
Initialize ICM20948 (IMU)
@params None
@return IMU instance
"""
def init_IMU():
	IMU = qwiic_icm20948.QwiicIcm20948()
	if IMU.connected == False:
		print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return None
	IMU.begin()
    
	IMU.getAgmt()
	accX = IMU.axRaw
	accY = IMU.ayRaw
	accZ = IMU.azRaw
	xRad = np.arctan2(-accY, -accZ)
	yRad = np.arctan2(-accX, -accZ)
	zRad = np.arctan2(-accY, -accX)

	initQuaternion = Quaternion(quaternion_from_euler(xRad, yRad, zRad))
	angles = MadgwickAHRS(sampleperiod=0.05, quaternion=initQuaternion)
	return (IMU, angles)


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


"""
Get IMU rotational data
@params IMU instance
@return [x_angle, y_angle, z_angle]
"""
def IMU_get_angle(my_IMU, angles, debug=False):
	if my_IMU == None:
		return None
	RAD_TO_DEG = 57.2957795
	if my_IMU.dataReady():
		my_IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables
		accX = my_IMU.axRaw
		accY = my_IMU.ayRaw
		accZ = my_IMU.azRaw
		gyroX = my_IMU.gxRaw/GYRO_SEN_FACTOR/RAD_TO_DEG
		gyroY = my_IMU.gyRaw/GYRO_SEN_FACTOR/RAD_TO_DEG
		gyroZ = my_IMU.gzRaw/GYRO_SEN_FACTOR/RAD_TO_DEG
		magX = my_IMU.mxRaw
		magY = my_IMU.myRaw
		magZ = my_IMU.mzRaw
		# x, y, z = filterUpdate(gyroX, gyroY, gyroZ, accX, accY, accZ)
		# angles.update_imu([gyroX, gyroY, gyroZ], [accX, accY, accZ])
		angles.update([gyroX, gyroY, gyroZ], [accX, accY, accZ], [magX, magY, magZ])
		x, y, z = angles.quaternion.to_euler_zyx()
		return [RAD_TO_DEG*x, RAD_TO_DEG*y, RAD_TO_DEG*z]
	else:
		print("Waiting for data")
	
