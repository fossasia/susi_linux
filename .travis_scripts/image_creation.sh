#!/bin/bash
cd /home/pi/

# if statement
if [ -d "SUSI.AI"]; 
then
    rm -rf SUSI.AI
fi

if [! -d "SUSI.AI"]; 
then
    mkdir SUSI.AI
fi

cd SUSI.AI

git clone https://github.com/fossasia/susi_linux

cd susi_linux/.travis_scripts/

chmod +x travis_install.sh

./travis_install.sh
