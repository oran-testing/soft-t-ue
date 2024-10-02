#!/bin/bash
# `install-ue.sh` -- Install the Test UE
#
# This script was originally written for Ubuntu 22 and has been adapted for Arch Linux.

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
	echo "This script must be run as root."
	exit 1
fi

PS4='[DEBUG] '
set -x

# Update and install build tools
pacman -Syu --noconfirm
pacman -S --needed --noconfirm cmake make gcc pkgconf fftw mbedtls libsctp yaml-cpp gtest zmq boost libconfig iperf3 git net-tools xcb-util-cursor mesa python python-pip mbedtls boost lksctp-tools libconfig

# Optional dependencies that may not be in official repositories, but you can try installing via AUR (if needed)
# Consider using an AUR helper like `yay` to install packages from the AUR
# yay -S gr-osmosdr

# Install Kivy and Kivy Garden's Graph via pip
pip install kivy kivy_garden.graph

# Install the software into /opt as per the Filesystem Hierarchy Standard
cd /opt

git clone https://github.com/oran-testing/soft-t-ue

# Build the srsRAN 4G with ZeroMQ enabled
cd soft-t-ue
mkdir -p build
cd build
cmake ../
make -j $(nproc)
make install

# Install srsRAN configurations
srsran_install_configs.sh user

set -x
