#! /bin/bash

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cd $DIR_PATH/../susi_server/susi_server/data/generic_skills/media_discovery/
 
sudo rm custom_skill.txt 
