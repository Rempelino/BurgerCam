#!/bin/bash
# Function to run a command in a new terminal window
run_in_terminal() {
    local title="$1"
    shift
    xterm -title "$title" -e bash -c "
    $*
    echo 'Process finished. Press any key to exit...'
    read -n 1 -s -r -p ''
    "
}
run_in_terminal "Burger Cam" "
echo \"----------------------------------------------------------------------------\"
echo \"---------------------------Starting Burger Cam------------------------------\"
echo \"----------------------------------------------------------------------------\"
cd ~/BurgerCam/backend
../venv/bin/python main.py
"