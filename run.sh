#!/bin/bash
# This script is to run SUSI.AI automatically at bootup
# The script is triggered through a Systemd rule `ss-factory-daemon.service`

cd "`dirname $0`"

nohup play wav/ting-ting_susi_is_alive_and_listening.wav &
python3 -m main
