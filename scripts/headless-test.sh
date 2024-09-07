#!/bin/bash

SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname $SCRIPT_PATH)

SESSION_1_NAME="gnb"
SESSION_1_COMMAND="gnb -c $SCRIPT_DIR/../configs/zmq/gnb_zmq.yaml"
SESSION_1_LOG="/tmp/tester_gnb.log"

SESSION_2_NAME="ue"
SESSION_2_COMMAND="srsue $SCRIPT_DIR/../configs/zmq/ue_zmq.conf $@"
SESSION_2_LOG="/tmp/soft_t_ue.log"

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

cd /opt/srsRAN_Project/docker/ && docker compose up --build 5gc -d

echo "waiting for open5gs..."
sleep 30

start_screen_session "$SESSION_1_NAME" "$SESSION_1_COMMAND" "$SESSION_1_LOG"
SESSION_1_STATUS=$?

ip netns add ue1

sleep 1

start_screen_session "$SESSION_2_NAME" "$SESSION_2_COMMAND" "$SESSION_2_LOG"
SESSION_2_STATUS=$?

# Check if both sessions were started successfully
if [ $SESSION_1_STATUS -ne 0 ] || [ $SESSION_2_STATUS -ne 0 ]; then
	echo "Failed to start screens"
	exit 1
fi

sleep 10
screen -ls
screen -S "ue" -X attach

kill_existing_screen "$SESSION_1_NAME"
kill_existing_screen "$SESSION_2_NAME"

cat $SESSION_1_LOG
cat $SESSION_2_LOG

if cat $SESSION_2_LOG | grep 'PDU Session'; then
	echo "T UE Connected successfully"
	exit 0
else
	echo "Connection Failed"
	exit 1
fi
