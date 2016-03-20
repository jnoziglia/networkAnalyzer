#!/bin/bash

for i in {1..10}
do
	nc -N 192.168.1.9 1234 < dummy1.html
	sleep $(( ( RANDOM % 10 ) + 1 ))
done