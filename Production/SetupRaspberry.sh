#!/bin/bash

check_internet() {
    ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1
}

try_connection() {
    local interface=$1
    local timeout=10
    local endtime=$(($(date +%s) + timeout))
    local connected=false
    echo "Trying to connect using $interface..."
    while [ $(date +%s) -lt $endtime ]; do
        if check_internet; then
            echo "$interface connected and internet accessible"
            connected=true
            break
        fi
        sleep 1
    done
    if [ "$connected" != true ]; then
        echo "$interface connection failed after $timeout seconds"
        return 1
    fi
    return 0
}

echo "----------------------------------------------------------------------------"
echo "---------------------------Checking internet connection---------------------"
echo "----------------------------------------------------------------------------"
echo ""

nmcli device disconnect eth0
nmcli radio wifi on
if try_connection "Wifi"; then
    echo "Using Wifi connection"
else
    echo "Wifi failed. Switching to Ethernet..."
    echo 'Turning on Ethernet...'
    nmcli device connect eth0
    nmcli radio wifi off
    
    if try_connection "Ethernet"; then
        echo "Using Ethernet connection"
    else
        echo "Both Ethernet and WiFi failed."
    fi
fi

if ! check_internet; then
    nmcli device connect eth0
    nmcli radio wifi on
    exit 1
fi

echo "----------------------------------------------------------------------------"
echo "---------------------------Updating pakage list-----------------------------"
echo "----------------------------------------------------------------------------"
sudo apt-get update

echo "----------------------------------------------------------------------------"
echo "---------------------------Downloading Project from github------------------"
echo "----------------------------------------------------------------------------"
sudo rm -rf BurgerCam
git clone https://github.com/Rempelino/BurgerCam.git

echo "----------------------------------------------------------------------------"
echo "---------------------------creating virtual enviroment----------------------"
echo "----------------------------------------------------------------------------"
sudo apt-get update
cd ~/BurgerCam/backend/ && python3 -m venv venv

echo "---------------------------------------------------------------------------"
echo "---------------------------downloading python pakages-----------------------"
echo "----------------------------------------------------------------------------"
cd ~/BurgerCam/backend && source venv/bin/activate && pip install -r requirements.txt

echo "---------------------------------------------------------------------------"
echo "---------------------------installing npm-------------------------------"
echo "----------------------------------------------------------------------------"
sudo apt install nodejs npm

echo "---------------------------------------------------------------------------"
echo "---------------------------setting up autostart procedure------------------"
echo "----------------------------------------------------------------------------"
sudo rm -rf ~/.config/autostart
sudo apt install xterm
cd ~/.config && mkdir "autostart"
cp ~/BurgerCam/Production/Execute.desktop ~/.config/autostart/
chmod +x ~/.config/autostart/Execute.desktop
chmod +x ~/BurgerCam/Production/Run.sh


sudo reboot




nmcli device connect eth0
nmcli radio wifi on