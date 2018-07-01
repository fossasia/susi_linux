#!/bin/bash

if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi

cd /etc/hostapd/
sed -i '1,14d' hostapd.conf

cd /etc/
sed -i '57,60d' dhcpcd.conf

cd /etc/network/
sed -i '9,17d' interfaces

#To remove the flask server file from auto-boot

cd /etc/
sed '$d' rc.local | sed '$d' rc.local | sed '$d' rc.local | sed '$d' rc.local
echo "" >> rc.local
echo "exit 0" >> rc.local
echo "" >> rc.local

echo "Please reboot"

sudo reboot
