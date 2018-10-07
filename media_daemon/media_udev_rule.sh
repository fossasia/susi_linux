#! /bin/bash
# To configure at bootup


SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)
RULE_NAME="99-susi-usb-drive.rules"

# Ref: https://unix.stackexchange.com/questions/229987/udev-rule-to-match-any-usb-storage-device
echo -e "\
ACTION==\"add\", KERNEL==\"sd?\", SUBSYSTEM==\"block\", ENV{ID_BUS}==\"usb\", RUN=\"$DIR_PATH/autostart.sh\"\n\
ACTION==\"remove\", KERNEL==\"sd?\", SUBSYSTEM==\"block\", ENV{ID_BUS}==\"usb\", RUN=\"$DIR_PATH/autostop.sh\"" > $DIR_PATH/$RULE_NAME

echo "Copy udev rules to trigger Media Discovery"
sudo cp $DIR_PATH/$RULE_NAME /etc/udev/rules.d/
