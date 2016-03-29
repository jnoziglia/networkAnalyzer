#!/bin/bash

# Copies repeatedly one of the resource files to every terminal, with a delay between 1 and 15 seconds between each transfer to the same terminal. 
# Uses scp command to copy the file over the network.

. ../config/ip_config.cfg

while [ true ]
do
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_1":~/linux.png >/dev/null 2>&1
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_2":~/linux.png >/dev/null 2>&1
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_3":~/linux.png >/dev/null 2>&1
	sleep $(( ( RANDOM % 15 ) + 1 ))
done
echo "Finished"