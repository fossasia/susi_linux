#! /bin/bash
SSID="$1"
PSK="$2"

if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi


if [[ $# -lt 1 ]]; 
	then echo "You need to pass a SSID!"
	echo "Usage:"
	echo "sudo $0 SSID PASSWORD"
	exit
fi

if [[ $# -lt 2 ]]; 
	then echo "You need to pass a PASSWORD!"
	echo "Usage:"
	echo "sudo $0 SSID PASSWORD"
	exit
fi

if [[ $# -gt 2 ]]; 
	then echo "You supplied an extra third command. Only two parameters needed!"
	echo "Usage:"
	echo "sudo $0 SSID PASSWORD"
	exit
fi

cat >> /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
network={
    ssid="$SSID"
    psk="$PSK"
}
EOF

echo "Connections configured, now reboot"
