# mobile-steering

## Installation
On PC, install `vgamepad` package by running

    pip install vgamepad

On RPi, install `nodejs` and `npm` package manager

    sudo su

    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

    sudo apt install nodejs

Verify the installation by

    node -- version
    npm --version

## Bluetooth Pairing
Make sure bluetooth is turned on on your PC. \
Then, ssh into RPi and run

    hciconfig

The bluetooth address is `xx:xx:xx:xx:xx:xx` in BD Address section. 

    hci0:   Type: Primary  Bus: UART
            BD Address: xx:xx:xx:xx:xx:xx  ACL MTU: 1021:8  SCO MTU: 64:1
            UP RUNNING 
            RX bytes:3482252 acl:11593 sco:0 events:1123 errors:0
            TX bytes:175593 acl:1076 sco:0 commands:121 errors:0


Copy that address to `pi/main.py` and replace it with the current `bd_addr` variable. \
In this setup, we are setting RPi as our server such that the bluetooth socket can bind to this address and listen for connection from PC. 


The following steps are copied from this [guide video](https://www.youtube.com/watch?v=DmtJBc229Rg) I found really useful. The steps are executed to pair RPi with PC. 

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

Then you will be able to find the device on PC and prompted to pair with RPi via bluetooth. 

Finally, we have to trust our PC this command on RPi, where `<PC MAC address>` is shown on the RPi console once connected

    trust <PC MAC address>

## Dashboard FPS
FPS refers to proximate frequency that the dashboard will update in a second. To change FPS, go to `pi/dashboard.py`. It basically controls the frequency of that `while` loop.
    
## Starting the Program
Firstly, make sure `bd_addr` variable is set to your RPi's bluetooth address in `main.py` and `dashboard.py` in both `pc` and `pi` folder.
### RPI
In `pi` folder and run the program that sends raw button inputs to PC

    python main.py

Then in another terminal at `pi/dashboard-backend` run following command to start the server that transfers outgauge data from python code to frontend

    npm start

Then in another terminal at `pi` folder run the following to start python program that receives outgauge data

    python dashboard.py

Finally, open `pi/dashboard-frontend/index.html` in the browser and set it to full screen to show the dashboard.

### PC
Start the game, make sure the Outgauge support at Options->Others is enabled.  The port should be `4444` and IP Address should be `127.0.0.1`. 

In `pc` folder run the following to receive the data from `pi` and control the game

    python main.py

Then, in another terminal run the following to write game data continuously to a file

    python outgauge.py


Finally, in another terminal run the following to read from the file and send data to RPi

    python dashboard.py




