#! /bin/bash

echo "running factory reset process"

# stop running processes
# killall python3
killall java

# extract backup
echo "extracting reset folder"
tar -Ipixz -C /home/pi/SUSI.AI/susi_linux/factory_reset/ -xf /home/pi/SUSI.AI/susi_linux/factory_reset/reset_folder.tar.xz

# replace running version with backup
echo "replacing the current version with the original version"
mv /home/pi/SUSI.AI/susi_linux/factory_reset/susi_linux /home/pi/SUSI.AI/susi_temp
mv /home/pi/SUSI.AI/susi_linux /home/pi/SUSI.AI/susi_old
mv /home/pi/SUSI.AI/susi_temp /home/pi/SUSI.AI/susi_linux

# rescue the rescue dump before cleaning up
echo "rescuing the rescue folder"
mv /home/pi/SUSI.AI/susi_old/factory_reset/reset_folder.tar.xz /home/pi/SUSI.AI/susi_linux/factory_reset/

# clean up
echo "cleaning up"
rm -rf /home/pi/SUSI.AI/susi_old

# prepare to run susi smart speaker as hot spot again
# here we undo the /home/pi/SUSI.AI/susi_linux/access_point/rwap.sh script
echo "restoring system definition files"
cp /etc/wpa_supplicant/wpa_supplicant.conf.bak /etc/wpa_supplicant/wpa_supplicant.conf
cp /etc/hostapd/hostapd.conf.bak /etc/hostapd/hostapd.conf
cp /etc/dhcpcd.conf.bak /etc/dhcpcd.conf
cp /etc/network/interfaces.bak /etc/network/interfaces

echo "enabling / disabling system services"
systemctl disable ss-startup-audio.service
systemctl disable ss-susi-linux.service
systemctl enable ss-python-flask.service
systemctl disable ss-susi-login.service

# restart
echo "reboot"
reboot
