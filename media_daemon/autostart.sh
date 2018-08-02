#! /bin/bash

clear

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cd $DIR_PATH/../susi_server/
if [ -d "susi_server" ]
then
    cd $DIR_PATH
    python3 auto_skills.py
else
    echo "Please download Skill Data"
fi 
