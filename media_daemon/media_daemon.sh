#! /bin/bash

clear

cd /etc/udev/rules.d
echo "ACTION==\"add\", RUN+=\"/home/pi/SUSI.AI/susi_linux/media_daemon/autostart.sh\"" >> 99-com.rules 
echo "ACTION==\"remove\", RUN+=\"/home/pi/SUSI.AI/susi_linux/media_daemon/autostop.sh\"" >> 99-com.rules 

sudo service udev restart

# python3 skill_script.py
