#! /bin/bash
# This script is executed during the installation process.
# This script mainly copies the local systemd the OS folder containing systemd files

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cp $DIR_PATH/Systemd/ss-update-daemon.service /lib/systemd/system/ss-update-daemon.service
cp $DIR_PATH/Systemd/ss-susi-server.service /lib/systemd/system/ss-susi-server.service
cp $DIR_PATH/Systemd/ss-python-flask.service /lib/systemd/system/ss-python-flask.service
cp $DIR_PATH/Systemd/ss-susi-linux.service /lib/systemd/system/ss-susi-linux.service
cp $DIR_PATH/Systemd/ss-susi-linux.service /lib/systemd/system/ss-factory-daemon.service

sudo systemctl daemon-reload
sudo systemctl enable ss-update-daemon.service
sudo systemctl enable ss-susi-server.service
sudo systemctl enable ss-python-flask.service
