#!/bin/bash
# # `install-ue.sh` -- Install the Test UE
#
# This script was written for Ubuntu 22. It may fail on any other OS/version.
#
# Check if the script is run as root:
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[DEBUG] '
set -x
# \
# **Install Docker:**
sudo apt install docker-compose
sudo apt install docker.io
# \
# Add Docker's official GPG key:
apt-get update
apt-get install -y ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
# \
# Install build tools:
apt-get update && apt-get upgrade -y
apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev
apt-get install -y libzmq3-dev
apt-get install -y net-tools libboost-all-dev libconfig++-dev iperf3 git libxcb-cursor0? libgles2-mesa-dev?
apt-get install -y gr-osmosdr python3 python3-pip
# \
# **Make and build:**
mkdir -p build
cd build
cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON
make -j $(nproc)
make install
# Sometimes Docker misbehaves and can be fixed with a simple restart:
sudo systemctl restart docker
# The status of Docker can be checked at anytime with: sudo systemctl status docker
cd ..
srsran_install_configs.sh user
cd docker
sudo docker compose build srsue

set -x
