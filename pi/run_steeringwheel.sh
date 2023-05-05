#! /usr/bin/bash
cd /home/steeringwheel/Desktop/steeringwheel/pi
xterm -e python main.py &
cd dashboard-backend
xterm -e npm start &
cd ../
xterm -e python dashboard.py &