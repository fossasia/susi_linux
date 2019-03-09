#! /bin/bash
SSID=""
PSK=""

if [ "$EUID" -ne 0 ]; then
  echo "Must be root"
  exit
fi

if [[ $# -gt 0 ]]; then
  SSID="$1"
fi

if [[ $# -gt 1 ]]; then
  PSK="$2"
fi

cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.bak

if [[ -z $SSID ]]; then
  echo "zero parameter, any open network"
  cat > /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    key_mgmt=NONE
    priority=-999
}
EOF
  exit
fi

if [[ -z $PSK ]]; then
  echo "open network $SSID"
  cat > /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="$SSID"
    key_mgmt=NONE
}
EOF
  exit
fi

echo "secure network $SSID"
cat > /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="$SSID"
    psk="$PSK"
}
EOF
