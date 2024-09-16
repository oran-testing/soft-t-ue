#!/bin/bash
# # `install-ue.sh` -- Install the Test UE
#
# This script was written for Ubuntu 22. It may fail on any other OS/version.

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[DEBUG] '
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
pip install kivy kivy_garden.graph

# We're installing an add-on application software package, which belongs in `/opt` per the [Filesystem Hierarchy Standard](https://www.pathname.com/fhs/pub/fhs-2.3.html#OPTADDONAPPLICATIONSOFTWAREPACKAGES).
cd /opt

git clone https://github.com/oran-testing/soft-t-ue

# [Build](https://docs.srsran.com/projects/4g/en/latest/app_notes/source/zeromq/source/index.html)
# the srsRAN 4G with ZeroMQ enabled.
cd soft-t-ue
mkdir -p build
cd build
cmake ../
make -j $(nproc)
make install
srsran_install_configs.sh user

set -x
