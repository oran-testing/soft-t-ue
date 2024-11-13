#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[install-gnb.sh] '
set -x

# Install build tools
apt-get update && apt-get upgrade -y
apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev
apt-get install -y libzmq3-dev
apt-get install -y net-tools libboost-all-dev libconfig++-dev iperf3 git libxcb-cursor0? libgles2-mesa-dev?

# Clone and install srsRAN

if [ -d /opt/srsRAN_Project/ ]; then
	echo "/opt/srsRAN_Project/ exists skipping"
else
	git clone https://github.com/oran-testing/srsRAN_Project.git /opt/srsRAN_Project/
fi

cd /opt/srsRAN_Project
mkdir -p build
cd build
cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON
make -j$(nproc)
make install

set -x
