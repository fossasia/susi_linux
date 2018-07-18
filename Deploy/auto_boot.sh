#! /bin/bash

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cp $DIR_PATH/ss-update-daemon.service /lib/systemd/system/ss-update-daemon.service

sudo systemctl daemon-reload
sudo systemctl enable ss-update-daemon.service
