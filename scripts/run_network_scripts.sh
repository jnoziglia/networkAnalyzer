#!/bin/bash

. ../config/ip_config.cfg

./network_script_scp.sh &
./network_script_rcp.sh &
./network_script_1.sh &