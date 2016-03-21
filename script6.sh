#!/bin/bash

for i in {1..20}
do
	sendip -p ipv4 -id 192.168.1.7 -p udp -us 5000 -ud 5000 -d "Hello" -v 192.168.1.7
	sleep $(( ( RANDOM % 5 ) + 1 ))
done
