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

	data = sock.recv(96)
	print("Data received")
	
	if not data:
		print('Lost connection.')
		break # Lost connection

	# Unpack the data.
	outsim_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)
	print(outsim_pack)
	
	time.sleep(1)
	print("test")
	
# Release the socket.
sock.close()

