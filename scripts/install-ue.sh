#!/bin/bash
# # `install-ue.sh` -- Install the Test UE
#
# This script was written for Ubuntu 22.04/20.04. It may fail on any other OS/version.

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[install-ue.sh] '
set -x

# Install build tools
#
# Install the required build tools for the
# [srsRAN 4G](https://docs.srsran.com/projects/4g/en/latest/general/source/1_installation.html#installation-from-source)
# and the
# [srsRAN project](https://docs.srsran.com/projects/project/en/latest/user_manuals/source/installation.html#manual-installation).
apt-get update && apt-get upgrade -y
apt-get install -y cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev
apt-get install -y libzmq3-dev
apt-get install -y net-tools libboost-all-dev libconfig++-dev iperf3 git libxcb-cursor0? libgles2-mesa-dev?
apt-get install -y gr-osmosdr python3 python3-pip

# [Build](https://docs.srsran.com/projects/4g/en/latest/app_notes/source/zeromq/source/index.html)
# the srsRAN 4G with ZeroMQ enabled.

if [ -d /opt/soft-t-ue ]; then
	echo "/opt/soft-t-ue exists skipping"
else
	git clone https://github.com/oran-testing/soft-t-ue /opt/soft-t-ue/
fi

cd /opt/soft-t-ue
mkdir -p build
cd build
cmake ../
make -j $(nproc)
make install
srsran_install_configs.sh user

set -x
