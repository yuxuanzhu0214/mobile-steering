# mobile-steering

## Software
### Installation
On PC, install `vgamepad` package by running

    pip install vgamepad


### Bluetooth Pairing
Make sure bluetooth is turned on on your laptop. \
Then, ssh into raspberry pi and run

    hciconfig

The bluetooth address in BD Address section. 

    hci0:   Type: Primary  Bus: UART
            BD Address: xx:xx:xx:xx:xx:xx  ACL MTU: 1021:8  SCO MTU: 64:1
            UP RUNNING 
            RX bytes:3482252 acl:11593 sco:0 events:1123 errors:0
            TX bytes:175593 acl:1076 sco:0 commands:121 errors:0


Copy that address to `pi/main.py` and replace it with the current `bd_addr` variable. \
In this setup, we are setting RPi as our server such that the bluetooth socket can bind to this address and listens for connections from PC.




## Installation

Instructions on how to install the project go here.

```bash
$ git clone https://github.com/username/project.git
$ cd project
$ npm install
