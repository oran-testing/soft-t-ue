#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[DEBUG] '
set -x

# Install build tools
apt-get update && apt-get upgrade -y
apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev
apt-get install -y libzmq3-dev
apt-get install -y net-tools libboost-all-dev libconfig++-dev iperf3 git libxcb-cursor0? libgles2-mesa-dev?

cd /opt

git clone https://github.com/oran-testing/soft-t-ue
cd soft-t-ue
mkdir -p build
cd build
cmake ../
make -j $(nproc)
make install
srsran_install_configs.sh user
cp ./srsue/src/srsue /usr/local/bin/

ip netns add ue1
ip netns list

set -x
