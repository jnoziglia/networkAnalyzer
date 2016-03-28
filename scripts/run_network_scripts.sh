#!/bin/bash

. ~/networkAnalyzer/config/ip_config.cfg

ssh ubuntu@"$ip_1" '~/networkAnalyzer/scripts/capture_script.sh &'
ssh ubuntu@"$ip_2" '~/networkAnalyzer/scripts/capture_script.sh &'
ssh ubuntu@"$ip_3" '~/networkAnalyzer/scripts/capture_script.sh &'
ssh ubuntu@"$ip_4" '~/networkAnalyzer/scripts/capture_script.sh &'
ssh ubuntu@"$ip_1" '~/networkAnalyzer/scripts/network_script_1.sh &'
ssh ubuntu@"$ip_2" '~/networkAnalyzer/scripts/network_script_1.sh &'
ssh ubuntu@"$ip_3" '~/networkAnalyzer/scripts/network_script_1.sh &'
ssh ubuntu@"$ip_4" '~/networkAnalyzer/scripts/network_script_1.sh &'
ssh ubuntu@"$ip_1" '~/networkAnalyzer/scripts/network_script_scp.sh &'
ssh ubuntu@"$ip_2" '~/networkAnalyzer/scripts/network_script_scp.sh &'
ssh ubuntu@"$ip_3" '~/networkAnalyzer/scripts/network_script_scp.sh &'
ssh ubuntu@"$ip_4" '~/networkAnalyzer/scripts/network_script_scp.sh &'
ssh ubuntu@"$ip_1" '~/networkAnalyzer/scripts/network_script_rcp.sh &'
ssh ubuntu@"$ip_2" '~/networkAnalyzer/scripts/network_script_rcp.sh &'
ssh ubuntu@"$ip_3" '~/networkAnalyzer/scripts/network_script_rcp.sh &'
ssh ubuntu@"$ip_4" '~/networkAnalyzer/scripts/network_script_rcp.sh &'