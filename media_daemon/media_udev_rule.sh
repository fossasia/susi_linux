#! /bin/bash
# To configure at bootup


SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

echo "Copy udev rules to trigger Media Discovery"
sudo cp $DIR_PATH/99-susi-usb-drive.rules /etc/udev/rules.d/

sudo service udev restart
