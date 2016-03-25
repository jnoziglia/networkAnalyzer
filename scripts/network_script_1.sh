#!/bin/bash

. ../ip_config.cfg

for i in {1..20}
do
	# sendip -p ipv4 -is "$my_ip" -id "$ip_1" -p udp -us 5000 -ud 5000 -d "Hello" -v "$ip_1"
	# sendip -p ipv4 -is "$my_ip" -id "$ip_2" -p udp -us 5000 -ud 5000 -d "Hello" -v "$ip_2"
	ping "$ip_1"
	ping "$ip_2"
	sleep $(( ( RANDOM % 5 ) + 1 ))
done
echo "Finished"
