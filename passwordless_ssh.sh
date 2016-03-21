#!/bin/bash

. ./ip_config.cfg

ssh-keygen -t rsa
scp ~/.ssh/id_rsa.pub ubuntu@"$ip_main":~/"$my_ip"