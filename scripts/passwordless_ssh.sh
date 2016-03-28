#!/bin/bash

. ../config/ip_config.cfg

ssh-keygen -t rsa
#scp ~/.ssh/id_rsa.pub ubuntu@"$ip_main":~/"$my_ip"
#scp ~/.ssh/id_rsa.pub ubuntu@"$ip_1":~/"$my_ip"
#scp ~/.ssh/id_rsa.pub ubuntu@"$ip_2":~/"$my_ip"

ssh ubuntu@"$ip_main" mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh ubuntu@"$ip_main" 'cat >> .ssh/authorized_keys'
ssh ubuntu@"$ip_main" "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

ssh ubuntu@"$ip_1" mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh ubuntu@"$ip_1" 'cat >> .ssh/authorized_keys'
ssh ubuntu@"$ip_1" "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

ssh ubuntu@"$ip_2" mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh ubuntu@"$ip_2" 'cat >> .ssh/authorized_keys'
ssh ubuntu@"$ip_2" "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

ssh ubuntu@"$ip_3" mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh ubuntu@"$ip_3" 'cat >> .ssh/authorized_keys'
ssh ubuntu@"$ip_3" "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"