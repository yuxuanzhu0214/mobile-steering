from __future__ import print_function
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_extended_bus import ExtendedI2C as I2C


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
	ADC_in_0 = AnalogIn(ADC, ADS.P0)
	ADC_in_1 = AnalogIn(ADC, ADS.P1)
	return ADC_in_0, ADC_in_1

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