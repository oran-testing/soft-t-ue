#!/bin/bash

PS4='[TEST: headless] '
set -x

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname $SCRIPT_PATH)
GNB_CONFIG=$SCRIPT_DIR/../configs/zmq/gnb_zmq.yaml
UE_CONFIG=$SCRIPT_DIR/../configs/zmq/ue_zmq.conf

CORE_SESSION_NAME="5gc"
CORE_SESSION_COMMAND="docker compose -f /opt/srsRAN_Project/docker/docker-compose.yml up --build 5gc"
CORE_SESSION_LOG="/tmp/headless_5gc.log"

GNB_SESSION_NAME="gnb"
GNB_SESSION_COMMAND="gnb -c $SCRIPT_DIR/../configs/zmq/gnb_zmq.yaml"
GNB_SESSION_LOG="/tmp/headless_gnb.log"

UE_SESSION_NAME="ue"
UE_SESSION_COMMAND="srsue $SCRIPT_DIR/../configs/zmq/ue_zmq.conf $@"
UE_SESSION_LOG="/tmp/headless_ue.log"

kill_existing_screen() {
	local session_name=$1
	if screen -list | grep -q "$session_name"; then
		screen -S "$session_name" -X quit
		if [ $? -ne 0 ]; then
			echo "Failed to kill existing screen session '$session_name'."
			return 1
		fi
	fi
	return 0
}

start_screen_session() {
	local session_name=$1
	local command=$2
	local log_file=$3
	screen -dmS "$session_name" bash -c "$command > $log_file 2>&1"
	if [ $? -ne 0 ]; then
		echo "Failed to start screen session '$session_name'."
		return 1
	fi
	return 0
}

ip netns add ue1 >/dev/null 2>&1

start_screen_session "$CORE_SESSION_NAME" "$CORE_SESSION_COMMAND" "$CORE_SESSION_LOG"
CORE_STATUS=$?

sleep 30

start_screen_session "$GNB_SESSION_NAME" "$GNB_SESSION_COMMAND" "$GNB_SESSION_LOG"
GNB_STATUS=$?

sleep 1

start_screen_session "$UE_SESSION_NAME" "$UE_SESSION_COMMAND" "$UE_SESSION_LOG"
UE_STATUS=$?

# Check if both sessions were started successfully
if [ $CORE_STATUS -ne 0 ] || [ $GNB_STATUS -ne 0 ] || [ $UE_STATUS -ne 0 ]; then
	echo "Failed to start screens"
	exit 1
fi

screen -ls
screen -S "ue" -X attach

kill_existing_screen "$UE_SESSION_NAME"
kill_existing_screen "$GNB_SESSION_NAME"
kill_existing_screen "$CORE_SESSION_NAME"

cat $UE_SESSION_LOG

if cat $SESSION_2_LOG | grep 'PDU Session'; then
	echo "T UE Connected successfully"
	exit 0
else
	echo "Connection Failed"
	exit 1
fi

set -x
