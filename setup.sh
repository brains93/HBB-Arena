#!/bin/bash
echo "Check if is root"
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

IP_ADDR=$(hostname -I)
WLANINT="wlan1"

# Add missing import statements
import pip
import apt

pip install -r ./requirements.txt
apt install dnsmasq hostapd

cp -r ./api "/var/www/html"
cp -r ./webapp "/var/www/html"

cat << EOF > /etc/systemd/system/arenaapi.service
[Unit]
Description=ArenaAPI
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/html/api
LimitNOFILE=4096
ExecStart=/usr/local/bin/uvicorn api:app --reload --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > /etc/systemd/system/arenaweb.service
[Unit]
Description=ArenaWeb
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/html/webapp
LimitNOFILE=4096
ExecStart=/usr/local/bin/flask --app app run --debug --host=0.0.0.0
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

EOF

systemctl daemon-reload
systemctl start arenaapi
systemctl start arenaweb
systemctl enable arenaweb
systemctl enable arenaapi
systemctl stop dnsmasq
systemctl stop hostapd

cat << EOF > /etc/dhcpcd.conf
interface $WLANINT
    static ip_address=192.168.80.1/24
    nohook wpa_supplicant
EOF

cat << EOF > /etc/dnsmasq.conf
interface=$WLANINT
dhcp-range=192.168.80.2,192.168.80.254,255.255.255.0,24h
EOF

cat << EOF > /etc/hostapd/hostapd.conf
country_code=GB
interface=$WLANINT
ssid=IBB_Arena
channel=9
auth_algs=1
wpa=2
wpa_passphrase=Activate!
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
EOF

cat << EOF > /etc/default/hostapd
interface=$WLANINT
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF

sed -i "s/^#DAEMON_CONF.*/DAEMON_CONF="/etc/hostapd/hostapd.conf"/" "/etc/default/hostapd"

systemctl start dnsmasq
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd
systemctl restart dhcpcd