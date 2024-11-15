#!/bin/bash
#
# # install-gnb.sh
#
# Check if the script is run as root:
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[DEBUG] '
INSTALL_DIR=$(pwd)
set -x

GNB_CONTROLLER_IP=$1
GNB_CONTROLLER_PORT=$2

SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname $SCRIPT_PATH)

cat <<EOF >/etc/systemd/system/gnb-controller.service
[Unit]
Description=gNB and Open5GS controller

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_DIR/../controller/gnb/main.py --ip $GNB_CONTROLLER_IP --port $GNB_CONTROLLER_PORT
Restart=always
User=root
Group=nogroup

[Install]
WantedBy=multi-user.target
EOF
# \
# Install build tools:
apt-get update && apt-get upgrade -y
apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev
apt-get install -y libzmq3-dev
apt-get install -y net-tools libboost-all-dev libconfig++-dev iperf3 git libxcb-cursor0? libgles2-mesa-dev?

set -x
