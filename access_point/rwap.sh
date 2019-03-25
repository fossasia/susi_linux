#!/bin/bash

if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi

# stop and disable hostapd, it cannot run once we have set up wifi
# and would be re-enabled in wap.sh if necessary
systemctl stop hostapd
systemctl disable hostapd

cd /etc/hostapd/
cp hostapd.conf hostapd.conf.bak
sed -i '1,14d' hostapd.conf

cd /etc/
cp dhcpcd.conf dhcpcd.conf.bak
sed -i '57,60d' dhcpcd.conf

cd /etc/network/
cp interfaces interfaces.bak
sed -i '9,17d' interfaces

#Empty port 5000
#Remove the server file from auto-boot
sudo systemctl enable ss-startup-audio.service
sudo systemctl enable ss-susi-linux.service
sudo systemctl disable ss-python-flask.service
sudo systemctl enable ss-susi-login.service

echo "Please reboot"
sleep 10;
sudo reboot
