#!/bin/sh
cp config_k8s_deployed.ini config_local.ini
python integration/controller.py
tail -f /dev/null
