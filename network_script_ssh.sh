#!/bin/bash

. ./ip_config.cfg

scp ./dummy1.html ubuntu@"$ip_1":~/dummy.html
scp ./dummy1.html ubuntu@"$ip_2":~/dummy.html
