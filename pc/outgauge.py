import socket
import struct
import time


print("Create UDP socket")
# Create UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Bind to BeamNG OutGauge")

# Bind to BeamNG OutGauge.
sock.bind(('127.0.0.1', 4444))
print("Binding successful")

while True:
	# Receive data.
	print("Receiving data")

	data = sock.recv(1024)
	print("Data received")
	
	if not data:
		print('Lost connection.')
		break # Lost connection

	# Unpack the data.
	outsim_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)
	print(outsim_pack)
	play_time = int(outsim_pack[0])
	name = str(outsim_pack[1])
	gear = str(outsim_pack[3])
	speed = float(outsim_pack[5]) #M/S
	rpm = float(outsim_pack[6])
	turbo = float(outsim_pack[7])
	engineTemp = float(outsim_pack[8])

	result = {}
	result["play_time"] = play_time
	result["name"] = name
	result["gear"] = gear
	result["speed"] = speed
	result["rpm"] = rpm
	result["turbo"] = turbo
	result["engineTemp"] = engineTemp
	print(result)
	
	# time.sleep(1)
	
# Release the socket.
sock.close()

