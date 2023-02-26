import socket
import struct



# Create UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to BeamNG OutGauge.
sock.bind(('127.0.0.1', 4444))

while True:
	# Receive data.
	data = sock.recv(96)

	if not data:
		break # Lost connection

	# Unpack the data.
	outsim_pack = struct.unpack('I4sH2c7f2I3f16s16si', data)
	
	print("RPM: ", str(outsim_pack[6])) 
	
# Release the socket.
sock.close()

