from __future__ import print_function
import qwiic_icm20948
import sys
import numpy as np


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
	return IMU

"""
Get IMU rotational data
@params IMU instance
@return [x_angle, y_angle, z_angle]
"""
def IMU_get_angle(my_IMU, debug=False):
	if my_IMU == None:
		return None
	RAD_TO_DEG = 57.2957795
	if my_IMU.dataReady():
		my_IMU.getAgmt() # read all axis and temp from sensor, note this also updates all instance variables
		accX = my_IMU.axRaw
		accY = my_IMU.ayRaw
		accZ = my_IMU.azRaw
		xAng = RAD_TO_DEG*(np.arctan2(-accY, -accZ))
		yAng = RAD_TO_DEG*(np.arctan2(-accX, -accZ))
		zAng = RAD_TO_DEG*(np.arctan2(-accY, -accX))
		if debug:
			print(\
				  'x:{: 06f}'.format(xAng)\
				 , '\t', 'y:{: 06f}'.format(yAng)\
				 , '\t', 'z:{: 06f}'.format(zAng)\
				 )
		return [xAng, yAng, zAng]
	else:
		print("IMU data not ready")
		return None
	
"""
Soft-reset IMU
@params IMU instance
@return None
"""
def IMU_reset(my_IMU):
	my_IMU.begin()