#!/bin/bash

. ./ip_config.cfg

tcpdump -i eth0 not arp and not rarp dst "$ip_1" or dst "$ip_2" -w - | ssh ubuntu@"$ip_main" 'cat >> output_new'