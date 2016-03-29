#!/bin/bash

# Merges files passed by argument when executing script and saves file to captures/output

. ../config/ip_config.cfg

mergecap "$@" -w ../captures/output