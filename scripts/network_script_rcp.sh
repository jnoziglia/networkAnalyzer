#!/bin/bash

. ~/networkAnalyzer/config/ip_config.cfg

while [ true ]
do
	rcp ~/networkAnalyzer/resources/dummy1.html ubuntu@"$ip_1":~/dummy.html >/dev/null 2>&1
	rcp ~/networkAnalyzer/resources/dummy1.html ubuntu@"$ip_2":~/dummy.html >/dev/null 2>&1
	rcp ~/networkAnalyzer/resources/dummy1.html ubuntu@"$ip_3":~/dummy.html >/dev/null 2>&1
	sleep $(( ( RANDOM % 5 ) + 1 ))
done
echo "Finished"