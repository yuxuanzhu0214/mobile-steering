"""
Scan/Discovery
--------------
Example showing how to scan for BLE devices.
Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>
"""

import asyncio

from bleak import BleakScanner


async def main():
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(return_adv=True)
    print(devices)

    for d, a in devices.values():
        print()
        print(d)
        print("-" * len(str(d)))
        print(a)


if __name__ == "__main__":
    asyncio.run(main())



# #!/usr/bin/env python3
# """
# A simple Python script to receive messages from a client over
# Bluetooth using Python sockets (with Python 3.3 or above).
# """
# # Bluetooth Addresses cmds: system_profiler SPBluetoothDataType, 
# # Mark's address: A4:83:E7:B1:CF:DB

# import socket

# hostMACAddress = 'A4:83:E7:B1:CF:DB' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
# port = 3 # port must match
# backlog = 1
# size = 1024
# s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# s.bind((hostMACAddress,port))
# s.listen(backlog)
# try:
#     print("Listening for client connection...")
#     client, address = s.accept()
#     while 1:
#         data = client.recv(size)
#         if data:
#             print(data)
#             client.send(data)
# except:	
#     print("Closing socket")	
#     client.close()
#     s.close()
