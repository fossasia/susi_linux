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

#Empty port 5000
#Remove the server file from auto-boot

echo "Please reboot"

sudo reboot
