#!/bin/bash

. ../config/ip_config.cfg

while [ true ]
do
	scp ../resources/linux.png ubuntu@"$ip_1":~/linux.png
	scp ../resources/linux.png ubuntu@"$ip_2":~/linux.png
	scp ../resources/linux.png ubuntu@"$ip_3":~/linux.png
	sleep $(( ( RANDOM % 15 ) + 1 ))
done
echo "Finished"