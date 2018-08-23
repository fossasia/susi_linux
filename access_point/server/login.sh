#! /bin/bash

SCRIPT_PATH=$(realpath $0)
DIR_PATH=$(dirname $SCRIPT_PATH)

AUTH="$1"
EMAIL="$2"
PASSWORD="$3"

cd $DIR_PATH/../../
sudo python3 authentication.py $AUTH $EMAIL $PASSWORD
