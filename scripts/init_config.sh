#!/bin/bash

# Installs dependencies and files needed for the system to work

apt-get -y install wireshark-common
apt-get -y install python3-pip
apt-get -y install python-pip
pip3 install yattag
pip install yattag
chmod u+x *.sh
apparmor_parser -R /etc/apparmor.d/usr.sbin.tcpdump