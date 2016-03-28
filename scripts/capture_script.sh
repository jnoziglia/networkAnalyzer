#!/bin/bash

# Script to start dumping process and save it to a file named as the host's IP

. ../config/ip_config.cfg

sudo tcpdump -i eth0 -s0 -U src "$ip_1" or src "$ip_2" or src "$ip_3" -w ~/networkAnalyzer/captures/"$my_ip"
