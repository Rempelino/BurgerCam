#!/bin/bash
# Function to run a command in a new terminal window
run_in_terminal() {
    local title="$1"
    shift
    xterm -title "$title" -e bash -c "
    $*
    echo 'Process finished'
    sleep 9
    "
}
run_in_terminal "Burger Cam" "
echo \"----------------------------------------------------------------------------\"
echo \"---------------------------Looking for Updates------------------------------\"
echo \"----------------------------------------------------------------------------\"
cd ~/BurgerCam
check_internet() {
    ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1
}
try_connection() {
    local interface=\$1
    local timeout=30
    local endtime=\$(( \$(date +%s) + timeout ))
    local connected=false
    echo \"Trying to connect using \$interface...\"
    while [ \$(date +%s) -lt \$endtime ]; do
        if check_internet; then
            echo \"\$interface connected and internet accessible\"
            connected=true
            break
        fi
        sleep 1
    done
    if [ \"\$connected\" != true ]; then
        echo \"\$interface connection failed after \$timeout seconds\"
        return 1
    fi
    return 0
}
# Try Ethernet first
if try_connection \"Ethernet\"; then
    echo \"Using Ethernet connection\"
else
    echo \"Ethernet failed. Switching to WiFi...\"
    nmcli device disconnect eth0
    echo 'Turning on WiFi...'
    nmcli radio wifi on
    
    if try_connection \"WiFi\"; then
        echo \"Using WiFi connection\"
    else
        echo \"Both Ethernet and WiFi failed. Proceeding without internet connection.\"
    fi
fi
# If we reach here, we either have an internet connection or both attempts failed
# Attempt to update and build only if we have an internet connection
if check_internet; then
    echo \"Checking for updates...\"
    git fetch
    if [ \$(git rev-parse HEAD) != \$(git rev-parse @{u}) ]; then
        echo \"Updates found. Pulling changes...\"
        git reset --hard
        git pull
	
	nmcli device connect eth0
	nmcli radio wifi off

        echo \"Changes pulled. Building frontend...\"
        cd frontend
        npm run build
    else
        echo \"No updates found. Skipping build.\"
    fi
else
    echo \"No internet connection. Skipping update and build.\"
fi
# Always enable Ethernet and turn off WiFi at the end, regardless of connection status
echo \"Enabling Ethernet and disabling WiFi...\"
nmcli device connect eth0
nmcli radio wifi off
echo \"Ethernet enabled and WiFi disabled.\"

echo \"----------------------------------------------------------------------------\"
echo \"---------------------------Starting Burger Cam------------------------------\"
echo \"----------------------------------------------------------------------------\"
cd ~/BurgerCam
venv/bin/python backend/main.py
"