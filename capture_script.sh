#!/bin/bash

. ./ip_config.cfg

tcpdump -i eth0 dst "$ip_1" or dst "$ip_2" not arp and not rarp -w - | ssh ubuntu@"$ip_main" 'cat >> output_new'