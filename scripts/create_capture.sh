#!/bin/bash

# Collects dump files from terminals, merges them into a single file and creates a text file out of the merged file

. ../config/ip_config.cfg

sftp ubuntu@"$ip_1":/home/ubuntu/networkAnalyzer/captures/"$ip_1"
sftp ubuntu@"$ip_2":/home/ubuntu/networkAnalyzer/captures/"$ip_2"
sftp ubuntu@"$ip_3":/home/ubuntu/networkAnalyzer/captures/"$ip_3"
sftp ubuntu@"$ip_4":/home/ubuntu/networkAnalyzer/captures/"$ip_4"
mergecap ./"$ip_1" ./"$ip_2" ./"$ip_3" ./"$ip_4" -w ../captures/output
tcpdump -nnv -r ../captures/output > ../captures/outputtxt