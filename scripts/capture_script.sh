#!/bin/bash

. ../ip_config.cfg

tcpdump -i eth0 src "$ip_1" or src "$ip_2" -w "$my_ip"
