#!/bin/bash

. ../ip_config.cfg

sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.tcpdump
mergecap ./"$ip_1" ./"$ip_2" ./"$ip_3" -w ../output
tcpdump -nnv -r ../output > ../outputtxt
