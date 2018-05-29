#! /bin/bash

clear

cd /home/pi/SUSI.AI/susi_linux/
if[ -d "susi_skill_data" ]
then
    cd /home/pi/SUSI.AI/susi_linux/susi_skill_data/models/custom/Music\ and\ Audio\ Accessories/en
    touch custom_audio.txt
else
    echo "Please download Skill Data"
fi