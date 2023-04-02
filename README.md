# mobile-steering

## Software
### Installation
On PC, install `vgamepad` package by running

    pip install vgamepad


### Bluetooth Pairing
Make sure bluetooth is turned on on your laptop. \
Then, ssh into RPi and run

    hciconfig

The bluetooth address is in BD Address section. 

    hci0:   Type: Primary  Bus: UART
            BD Address: xx:xx:xx:xx:xx:xx  ACL MTU: 1021:8  SCO MTU: 64:1
            UP RUNNING 
            RX bytes:3482252 acl:11593 sco:0 events:1123 errors:0
            TX bytes:175593 acl:1076 sco:0 commands:121 errors:0


Copy that address to `pi/main.py` and replace it with the current `bd_addr` variable. \
In this setup, we are setting RPi as our server such that the bluetooth socket can bind to this address and listen for connection from PC. 


The following steps are copied from this [guide video](https://www.youtube.com/watch?v=DmtJBc229Rg) I found really useful. The steps are executed to pair RPi with laptop. 

On RPi, run the following command

    sudo nano /lib/systemd/system/bluetooth.service

Add a `-C` after `/usr/libexec/bluetooth/bluetoothd` in `ExecStart` so it looks like

    ExecStart=/usr/libexec/bluetooth/bluetoothd -C

Save the file and reboot RPi by running 

    sudo reboot

After robooting, run

    sudo service bluetooth status

Make sure the `CGroup` field looks like the following

    CGroup: /system.slice/bluetooth.service
        └─804 /usr/libexec/bluetooth/bluetoothd -C

Then, enter the command to start pairing

    sudo bluetoothctl

In the console, run the following commands one by one

    power on
    pairable on
    discoverable on
    agent on
    default-agent

Then you will be able to find the device on laptop and prompted to pair with RPi via bluetooth. 

Finally, we have to trust our laptop this command on RPi

    trust <laptop MAC address>
    
### Starting the Program
On RPi, `cd` into `pi` folder and run

    python main.py

On laptop, `cd` into `pc` folder and run

    python main.py



