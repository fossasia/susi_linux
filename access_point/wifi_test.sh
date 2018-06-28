#! /bin/bash

WIFI_ON=''

if nc -zw1 google.com 443
then 
    echo "connection successful"
    WIFI_ON='1'
elif ping -q -t 5 -w1 -c1 8.8.8.8 t
then
    echo "connection successful"
    WIFI_ON='1'
elif wget -q --spider http://google.com
then 
    echo "connection successful"
    WIFI_ON='1'
else
    echo "wifi not connected"
    WIFI_ON='0'
fi

if [ $WIFI_ON=='1' ]
then 
    echo "connection successful"
else
    echo "wifi not connected"
    sudo ./wap.sh
fi
