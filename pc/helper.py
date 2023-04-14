import struct

def read_outauge(data):
    # Unpack the data.
	outsim_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)
	print(outsim_pack)
	gear = str(outsim_pack[3])
	speed = float(outsim_pack[5]) #M/S
	rpm = float(outsim_pack[6])

	result = {}
	result["gear"] = gear
	result["speed"] = int(speed * 3.6)
	result["rpm"] = int(rpm)
	return result