cd "`dirname $0`"

# to run this script after a start-up of a raspberry py,
# add the following line to /etc/rc.local
#
# nohup su - pi /home/pi/git/susi_linux/run.sh &
#
# then you get a fully self-contained assistant appliance which
# announces readyness status with one text line "alive and listening"
#
# This requires, that susi is installed in
# /home/pi/git/susi_linux

nohup play wav/ting-ting_susi_is_alive_and_listening.wav &
python3 -m main
