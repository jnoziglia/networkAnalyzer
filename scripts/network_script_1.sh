#!/bin/bash

. ~/networkAnalyzer/config/ip_config.cfg

while [ true ]
do
	ping -c 1 "$ip_1" >/dev/null 2>&1
	ping -c 1  "$ip_2" >/dev/null 2>&1
	ping -c 1  "$ip_3" >/dev/null 2>&1
done
echo "Finished"
