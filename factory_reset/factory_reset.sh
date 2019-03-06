#! /bin/bash

# extract backup
sudo tar -Ipixz -C $DIR_PATH/ -xf $DIR_PATH/reset_folder.tar.xz

# stop running processes
sudo killall python3
sudo killall java

# replace running version with backup
mv /home/pi/SUSI.AI/susi_linux/factory_reset/susi_linux /home/pi/SUSI.AI/susi_temp
mv /home/pi/SUSI.AI/susi_linux /home/pi/SUSI.AI/susi_old
mv /home/pi/SUSI.AI/susi_temp /home/pi/SUSI.AI/susi_linux

# clean up
rm -rf /home/pi/SUSI.AI/susi_old

# prepare to run susi smart speaker as hot spot again
sudo bash /home/pi/SUSI.AI/susi_linux/access_point/wap.sh

# restart
sudo shutdown -r now
