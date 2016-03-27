#!/bin/bash

. ~/networkAnalyzer/config/ip_config.cfg

while [ true ]
do
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_1":~/linux.png >/dev/null 2>&1
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_2":~/linux.png >/dev/null 2>&1
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_3":~/linux.png >/dev/null 2>&1
	sleep $(( ( RANDOM % 15 ) + 1 ))
done
echo "Finished"