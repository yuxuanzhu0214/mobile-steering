from __future__ import print_function
import qwiic_icm20948
import time
import sys
import board
import digitalio
import busio
import adafruit_ads1x15.ads1115 as ADS
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_extended_bus import ExtendedI2C as I2C

from pi.ADC import *

#from test_buttons import *

"""
Initialize ADS1115 (ADC)
@params None
@return ADC channel instance
"""
def init_ADC():
	i2c = I2C(2)
	print("I2C ok!")
	# Create the ADC object using the I2C bus
	ADC = ADS.ADS1115(i2c)
	# Create single-ended input on channel 0
	ADC_in = AnalogIn(ADC, ADS.P0)
	return ADC_in

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
	
"""
Get ADC voltage input data
@params ADC instance
@return V_in
"""
def ADC_get_input(my_ADC, debug=False):
	V_in = my_ADC.voltage
	if debug:
		print("pot:{:>5.3f}".format(V_in))
	return V_in

def runTest(debug=False):

	ADC_in = init_ADC()

	IMU = init_IMU()

	while True:
		xyz_angle = IMU_get_angle(IMU, debug)
		pot_v_in = ADC_get_input(ADC_in, debug)
		
		time.sleep(0.5)

if __name__ == '__main__':
	try:
		runTest(True)
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nBye")
		sys.exit(0)

