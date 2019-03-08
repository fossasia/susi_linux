#! /bin/bash

# extract backup
tar -Ipixz -C /home/pi/SUSI.AI/susi_linux/factory_reset/ -xf /home/pi/SUSI.AI/susi_linux/factory_reset/reset_folder.tar.xz

# stop running processes
sudo killall python3
sudo killall java

# replace running version with backup
mv /home/pi/SUSI.AI/susi_linux/factory_reset/susi_linux /home/pi/SUSI.AI/susi_temp
mv /home/pi/SUSI.AI/susi_linux /home/pi/SUSI.AI/susi_old
mv /home/pi/SUSI.AI/susi_temp /home/pi/SUSI.AI/susi_linux

# rescue the rescue dump
mv /home/pi/SUSI.AI/susi_old/factory_reset/reset_folder.tar.xz /home/pi/SUSI.AI/susi_linux/factory_reset/

# clean up
sudo rm -rf /home/pi/SUSI.AI/susi_old

# prepare to run susi smart speaker as hot spot again
# here we undo the /home/pi/SUSI.AI/susi_linux/access_point/rwap.sh script
cd /etc/hostapd/
sudo cp hostapd.conf.bak hostapd.conf
cd /etc/
sudo cp dhcpcd.conf.bak dhcpcd.conf
cd /etc/network/
sudo cp interfaces.bak interfaces

sudo systemctl disable ss-startup-audio.service
sudo systemctl disable ss-susi-linux.service
sudo systemctl enable ss-python-flask.service
sudo systemctl disable ss-susi-login.service

# restart
sudo reboot
