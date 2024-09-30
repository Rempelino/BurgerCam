#!/bin/bash

# Function to run a command in a new terminal window
run_in_terminal() {
    local title="$1"
    shift
    xterm -title "$title" -e bash -c "$*; echo 'Press Enter to close'; read" &
}

# Change to BurgerCam directory and pull latest changes
# cd /home/henry/BurgerCam && git pull --all

# Run backend
run_in_terminal "BurgerCam Backend" "cd /home/henry/BurgerCam/backend && venv/bin/python main.py"

# Run frontend
# run_in_terminal "BurgerCam Frontend" "cd /home/henry/BurgerCam/frontend && BG_CLI_ANALYTICS=false ng serve"

# Keep the script running
wait