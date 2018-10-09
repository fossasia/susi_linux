#!/bin/bash

sudo apt-get install qemu

git clone https://github.com/dhruvvyas90/qemu-rpi-kernel.git

qemu-img convert -f raw -O qcow2 2017-08-16-raspbian-stretch-lite.zip raspbian-stretch-lite.qcow

qemu-img resize raspbian-stretch-lite.qcow +6G

sudo qemu-system-arm \
-kernel ./kernel-qemu-4.9.59-stretch \
-append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" \
-hda raspbian-stretch-lite.qcow \
-cpu arm1176 -m 256 \
-M versatilepb \
-no-reboot \
-serial stdio \
-net nic -net user \
-net tap,ifname=vnet0,script=no,downscript=no

cd ~/
mkdir SUSI.AI
git clone https://github.com/fossasia/susi_linux
cd susi_linux/
sudo bash ~/SUSI.AI/susi_linux/.travis_scripts/install.sh
