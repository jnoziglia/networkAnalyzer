#!/bin/bash

. ../ip_config.cfg

sftp ubuntu@"$ip_1":/home/ubuntu/networkAnalyzer/captures/"$ip_1"
sftp ubuntu@"$ip_1":/home/ubuntu/networkAnalyzer/captures/"$ip_2"
sftp ubuntu@"$ip_1":/home/ubuntu/networkAnalyzer/captures/"$ip_3"
mergecap ./"$ip_1" ./"$ip_2" ./"$ip_3" -w ../output
tcpdump -nnv -r ../output > ../outputtxt