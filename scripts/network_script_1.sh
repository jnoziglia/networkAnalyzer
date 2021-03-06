#!/bin/bash

# Sends an echo request (PING) to every terminal every 10 seconds.

. ../config/ip_config.cfg

while [ true ]
do
	ping -c 1 "$ip_1" >/dev/null 2>&1
	ping -c 1  "$ip_2" >/dev/null 2>&1
	ping -c 1  "$ip_3" >/dev/null 2>&1
	sleep 10
done
echo "Finished"
