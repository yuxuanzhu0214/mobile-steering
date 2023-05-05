from __future__ import print_function
import time
import sys

from pi.ADC import *
from IMU import *

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

