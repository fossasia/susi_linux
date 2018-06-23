#! /bin/bash

clear

cd $HOME/SUSI.AI/susi_linux/
if [ -d "susi_server" ]
then
    cd $HOME/SUSI.AI/susi_linux/media_daemon/
    python3 auto_skills.py
else
    echo "Please download Skill Data"
fi 
