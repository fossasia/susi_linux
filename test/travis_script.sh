#!/bin/bash

mkdir QEMU
cd QEMU

# Downloading and installing QEMU from the source
wget https://download.qemu.org/qemu-2.12.0-rc0.tar.xz
tar xvJf qemu-2.12.0-rc0.tar.xz
cd qemu-2.12.0-rc0
./configure --target-list=arm-softmmu,aarch64-softmmu
make

# Downloading the latest Raspbian image
wget https://downloads.raspberrypi.org/raspbian_lite_latest
mv raspbian_lite_latest raspbian_lite_latest.zip
unzip raspbian_lite_latest.zip

qemu-img convert -f raw -O qcow2 2018-10-09-raspbian-stretch-lite.img raspbian-lite.qcow2

qemu-img resize raspbian-lite.qcow2 +8G

# Downloading the kernel
wget https://github.com/dhruvvyas90/qemu-rpi-kernel/raw/master/kernel-qemu-4.4.34-jessi


qemu-system-arm \
        -kernel /kernel-qemu-4.4.34-jessie \
        -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" \
        -hda /raspbian-lite.qcow2 \
        -cpu arm1176 \
        -m 256 \
        -machine versatilepb
