#!/bin/bash
# Define functions
check_internet() {
    ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1
}
try_connection() {
    local interface=$1
    local timeout=30
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
echo "---------------------------Looking for Updates------------------------------"
echo "----------------------------------------------------------------------------"
# Try Ethernet first
if try_connection "Ethernet"; then
    echo "Using Ethernet connection"
else
    echo "Ethernet failed. Switching to WiFi..."
    nmcli device disconnect eth0
    echo 'Turning on WiFi...'
    nmcli radio wifi on

    if try_connection "WiFi"; then
        echo "Using WiFi connection"
    else
        echo "Both Ethernet and WiFi failed. Proceeding without internet connection."
    fi
fi
# If we reach here, we either have an internet connection or both attempts failed
# Attempt to update and build only if we have an internet connection
if check_internet; then
    echo "Checking for updates..."
    cd ~/BurgerCam && git fetch
    if [ $(cd ~/BurgerCam && git rev-parse HEAD) != $(cd ~/BurgerCam && git rev-parse @{u}) ]; then
        echo "Updates found. Pulling changes..."
        cd ~/BurgerCam && git reset --hard
        cd ~/BurgerCam && git pull
        echo "Changes pulled. Building frontend..."
        sudo rm -rf ~/BurgerCam/Production/frontend
        cd ~/BurgerCam/frontend && npm run build
        # Check if the build was successful
        if [ $? -eq 0 ]; then
            echo "Frontend build successful. Moving dist folder..."
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

    else
        echo "No updates found. Skipping build."
    fi
else
    echo "No internet connection. Skipping update and build."
fi
# Always enable Ethernet and turn off WiFi at the end, regardless of connection status
echo "Enabling Ethernet and disabling WiFi..."
nmcli device connect eth0
nmcli radio wifi off

# make scripts executable just in case
chmod +x ~/BurgerCam/Production/Run.sh
chmod +x ~/BurgerCam/Production/SearchForUpdates.sh
chmod +x ~/BurgerCam/Production/RunBurgerCam.sh

echo "Ethernet enabled and WiFi disabled."
