#!/bin/bash

# Install required packages
apt-get install -y sudo iputils-ping

# Create TUN device
mkdir -p /dev/net
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun

# Run OpenVPN
openvpn --config /workdir/lab.ovpn --daemon
