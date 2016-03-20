#!/bin/bash

for i in {1..10}
do
	sendip -p ipv4 -is 192.168.1.10 -id 192.168.1.9 -p udp -us 5070 -ud 5060 -d "Hello" -v 192.168.1.9
	sleep $(( ( RANDOM % 10 ) + 1 ))
done