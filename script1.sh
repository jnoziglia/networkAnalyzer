#!/bin/bash

for i in {1..20}
do
	sendip -p ipv4 -is 192.168.1.10 -id 192.168.1.9 -p udp -us 5000 -ud 5000 -d "Hello" -v 192.168.1.9
	sleep $(( ( RANDOM % 5 ) + 1 ))
done
