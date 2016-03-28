#!/bin/bash

# Script to run all the network traffic generator scripts simultaneously
# Runs on terminals

. ../config/ip_config.cfg

./network_script_scp.sh &
./network_script_rcp.sh &
./network_script_1.sh &