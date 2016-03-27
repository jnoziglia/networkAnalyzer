#!/bin/bash

. ../config/ip_config.cfg

while [ true ]
do
	rcp ../resources/dummy1.html ubuntu@"$ip_1":~/dummy.html
	rcp ../resources/dummy1.html ubuntu@"$ip_2":~/dummy.html
	rcp ../resources/dummy1.html ubuntu@"$ip_3":~/dummy.html
	sleep $(( ( RANDOM % 5 ) + 1 ))
done
echo "Finished"