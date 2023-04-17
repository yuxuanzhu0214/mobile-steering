import struct

def read_outauge(data):
    # Unpack the data.
	outsim_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)
	# print(outsim_pack)
	gear = ord(outsim_pack[3])
	speed = int(float(outsim_pack[5]) * 3.6) #M/S
	rpm = int(float(outsim_pack[6]))

	result = [speed, rpm, gear]
	return result