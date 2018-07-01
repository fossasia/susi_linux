#! /bin/bash
# Configuring the Update Daemon and the flask server to start on bootup

cd /etc/
sed 'N;$!P;$!D;$d' rc.local
echo "sudo bash $HOME/SUSI.AI/susi_linux/update_daemon &" >> rc.local
echo "sudo python $HOME/SUSI.AI/susi_linux/access_point/server/server.py &" >> rc.local
echo "" >> rc.local
echo "exit 0" >> rc.local
echo "" >> rc.local
