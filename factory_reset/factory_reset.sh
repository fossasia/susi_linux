#! /bin/bash

# stop running processes
killall python3
killall java

# extract backup
tar -Ipixz -C /home/pi/SUSI.AI/susi_linux/factory_reset/ -xf /home/pi/SUSI.AI/susi_linux/factory_reset/reset_folder.tar.xz

# replace running version with backup
mv /home/pi/SUSI.AI/susi_linux/factory_reset/susi_linux /home/pi/SUSI.AI/susi_temp
mv /home/pi/SUSI.AI/susi_linux /home/pi/SUSI.AI/susi_old
mv /home/pi/SUSI.AI/susi_temp /home/pi/SUSI.AI/susi_linux

# rescue the rescue dump before cleaning up
mv /home/pi/SUSI.AI/susi_old/factory_reset/reset_folder.tar.xz /home/pi/SUSI.AI/susi_linux/factory_reset/

# clean up
rm -rf /home/pi/SUSI.AI/susi_old

# prepare to run susi smart speaker as hot spot again
# here we undo the /home/pi/SUSI.AI/susi_linux/access_point/rwap.sh script
cp /etc/hostapd/hostapd.conf.bak /etc/hostapd/hostapd.conf
cp /etc/dhcpcd.conf.bak /etc/dhcpcd.conf
cp /etc/network/interfaces.bak /etc/network/interfaces

systemctl disable ss-startup-audio.service
systemctl disable ss-susi-linux.service
systemctl enable ss-python-flask.service
systemctl disable ss-susi-login.service

# restart
reboot
