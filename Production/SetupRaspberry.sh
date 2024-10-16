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

echo "---------------------------------------------------------------------------"
echo "---------------------------Updating pakage list----------------------------"
echo "---------------------------------------------------------------------------"
sudo apt-get update

echo "---------------------------------------------------------------------------"
echo "---------------------------Downloading Project from github-----------------"
echo "---------------------------------------------------------------------------"
sudo rm -rf BurgerCam
echo "removed directory BurgerCam"
git clone https://github.com/Rempelino/BurgerCam.git

echo "---------------------------------------------------------------------------"
echo "---------------------------creating virtual enviroment---------------------"
echo "---------------------------------------------------------------------------"
cd ~/BurgerCam/backend/ && python3 -m venv venv

echo "---------------------------------------------------------------------------"
echo "---------------------------downloading python pakages----------------------"
echo "---------------------------------------------------------------------------"
cd ~/BurgerCam/backend && source venv/bin/activate && pip install -r requirements.txt

echo "---------------------------------------------------------------------------"
echo "---------------------------installing npm----------------------------------"
echo "---------------------------------------------------------------------------"
sudo apt install nodejs npm

echo "---------------------------------------------------------------------------"
echo "---------------------------installing pakages------------------------------"
echo "---------------------------------------------------------------------------"
cd ~/BurgerCam/frontend && npm install

echo "---------------------------------------------------------------------------"
echo "---------------------------building frontend-------------------------------"
echo "---------------------------------------------------------------------------"
cd ~/BurgerCam/frontend && npm run build
# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Frontend build successful. Moving dist folder..."
    sudo rm -rf ~/BurgerCam/Production/frontend
    mv ~/BurgerCam/frontend/dist/frontend ~/BurgerCam/Production
    
    # Check if the move was successful
    if [ $? -eq 0 ]; then
        echo "Successfully moved dist folder to the destination."
    else
        echo "Failed to move dist folder. Please check permissions and paths."
    fi
else
    echo "Frontend build failed. Dist folder will not be moved."
fi

echo "---------------------------------------------------------------------------"
echo "---------------------------setting up autostart procedure------------------"
echo "---------------------------------------------------------------------------"
sudo rm -rf ~/.config/autostart
sudo apt install xterm
cd ~/.config && mkdir "autostart"
cp ~/BurgerCam/Production/Execute.desktop ~/.config/autostart/
chmod +x ~/.config/autostart/Execute.desktop
chmod +x ~/BurgerCam/Production/Run.sh
chmod +x ~/BurgerCam/Production/SearchForUpdates.sh
chmod +x ~/BurgerCam/Production/RunBurgerCam.sh

echo "---------------------------------------------------------------------------"
echo "-----------------installing Galaxy Viewer (required for cam driver)--------"
echo "---------------------------------------------------------------------------"
cd ~/BurgerCam/GalaxyViewerLinux && chmod +x Galaxy_camera.run
cd ~/BurgerCam/GalaxyViewerLinux && sudo ./Galaxy_camera.run

nmcli device connect eth0
nmcli radio wifi on

read -n 1 -s -r -p 'Process finished. Press any key to reboot the pi'
sudo reboot