#!/bin/bash

. ~/networkAnalyzer/config/ip_config.cfg

while [ true ]
do
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_1":~/linux.png
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_2":~/linux.png
	scp ~/networkAnalyzer/resources/linux.png ubuntu@"$ip_3":~/linux.png
	sleep $(( ( RANDOM % 15 ) + 1 ))
done
echo "Finished"