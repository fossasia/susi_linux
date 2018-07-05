#! /bin/bash
# To configure at bootup

clear

echo "Copy udev rules to trigger Media Discovery"
sudo cp ./media_daemon/99-susi-usb-drive.rules /etc/udev/rules.d/

sudo service udev restart
