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

# Main script
echo "----------------------------------------------------------------------------"
echo "---------------------------Starting Burger Cam------------------------------"
echo "----------------------------------------------------------------------------"

# Check if the frontend directory does not exist
if [ ! -d ~/BurgerCam/Production/frontend ]; then
    nmcli device disconnect eth0
    nmcli radio wifi on
    if try_connection "Wifi"; then
        echo "Using Wifi connection"
    else
        echo "Wifi failed. Switching to Ethernet..."
        echo "Turning on Ethernet..."
        nmcli device connect eth0
        nmcli radio wifi off
    
        if try_connection "Ethernet"; then
            echo "Using Ethernet connection"
        else
            echo "Both Ethernet and WiFi failed."
        fi
    fi

    if check_internet; then
        cd ~/BurgerCam/frontend && npm run build
        BUILD_EXIT_CODE=$?
    
        # Check if the build was successful
        if [ $BUILD_EXIT_CODE -eq 0 ] && [ -d ~/BurgerCam/frontend/dist ]; then
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
    fi
fi

nmcli device connect eth0
nmcli radio wifi on
cd ~/BurgerCam/backend && sudo venv/bin/python main.py
