#!/bin/bash

. ../config/ip_config.cfg

tcpdump -i eth0 src "$ip_1" or src "$ip_2" or src "$ip_3" -w ../captures/"$my_ip"
