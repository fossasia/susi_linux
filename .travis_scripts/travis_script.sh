#!/bin/bash

mkdir QEMU
cd QEMU

# Downloading and installing QEMU from the source
wget https://download.qemu.org/qemu-2.12.0-rc0.tar.xz
tar xvJf qemu-2.12.0-rc0.tar.xz
cd qemu-2.12.0-rc0
./configure --target-list=arm-softmmu,aarch64-softmmu
make

sudo apt-get install qemu qemu-system-arm qemu-img

# Downloading the latest Raspbian Qcow
wget http://download1476.mediafire.com/c6awtxzajfwg/yujb71p1d2q19k2/raspbian-lite.qcow2

qemu-img resize raspbian-lite.qcow2 +8G

# Downloading the kernel
wget https://github.com/dhruvvyas90/qemu-rpi-kernel/raw/master/kernel-qemu-4.4.34-jessie


qemu-system-arm \
        -kernel ./kernel-qemu-4.4.34-jessie \
        -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" \
        -hda ./raspbian-lite.qcow2 \
        -cpu arm1176 \
        -m 256 \
        -machine versatilepb
