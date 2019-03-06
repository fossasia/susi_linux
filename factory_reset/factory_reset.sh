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
sudo bash /home/pi/SUSI.AI/susi_linux/access_point/wap.sh

# restart: the wap script is doing the restart
