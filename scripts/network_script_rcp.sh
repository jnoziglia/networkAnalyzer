#!/bin/bash

# Copies repeatedly one of the resource files to every terminal, with a delay between 1 and 5 seconds between each transfer to the same terminal. 
# Uses rcp command to copy the file over the network.

. ../config/ip_config.cfg

while [ true ]
do
	rcp ~/networkAnalyzer/resources/dummy1.html ubuntu@"$ip_1":~/dummy.html >/dev/null 2>&1
	rcp ~/networkAnalyzer/resources/dummy1.html ubuntu@"$ip_2":~/dummy.html >/dev/null 2>&1
	rcp ~/networkAnalyzer/resources/dummy1.html ubuntu@"$ip_3":~/dummy.html >/dev/null 2>&1
	sleep $(( ( RANDOM % 5 ) + 1 ))
done
echo "Finished"