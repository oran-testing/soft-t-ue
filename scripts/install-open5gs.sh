#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[DEBUG] '
set -x

sudo apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev ##
sudo apt install docker-compose																							##
sudo apt install docker.io																								##

# Add Docker's official GPG key:
apt-get update
apt-get install -y ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
	"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |
	tee /etc/apt/sources.list.d/docker.list >/dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

##cd /opt
pwd
cd ..
pwd
# Clone and install srsRAN
##git clone https://github.com/oran-testing/srsRAN_Project.git
cd srsRAN_Project
##git checkout ue-tester
cd docker
sudo systemctl restart docker
sudo docker compose build 5gc
sudo docker compose up 5gc

set -x
