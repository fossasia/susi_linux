#! /bin/bash
AUTH="$1"
EMAIL="$2"
PASSWORD="$3"

cd /home/pi/SUSI.AI/susi_linux/
sudo python3 authentication.py $AUTH $EMAIL $PASSWORD
