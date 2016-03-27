#!/bin/bash

. ~/networkAnalyzer/config/ip_config.cfg

while [ true ]
do
	ping -c 1 "$ip_1"
	ping -c 1  "$ip_2"
	ping -c 1  "$ip_3"
done
echo "Finished"
