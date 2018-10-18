#! /bin/bash
# This script is executed during the installation process.
# This script is to install systemd service files.

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

cp $DIR_PATH/Systemd/ss-*.service /lib/systemd/system/

systemctl enable ss-update-daemon.service
systemctl enable ss-susi-server.service
systemctl enable ss-python-flask.service
systemctl enable ss-susi-youtube.service
