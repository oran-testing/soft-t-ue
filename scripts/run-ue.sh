#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

function run_screen {
	local screen_name="$1"
	local command_to_run="$2"

	# Check if screen session already exists
	if screen -list | grep -q "\.$screen_name"; then
		echo "Screen session '$screen_name' already exists."
	else
		# Start a new screen session with the given name
		screen -dmS "$screen_name"
		echo "Started screen session '$screen_name'."
	fi

	# Execute the command within the screen session
	screen -S "$screen_name" -p 0 -X stuff "$command_to_run$(printf \\r)"
	echo "Started process '$command_to_run' in screen session '$screen_name'."
}

run_screen "srsRAN tester UE" "srsue"
