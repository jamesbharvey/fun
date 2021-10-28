#!/bin/bash

logdir=$(dirname $0)

ping -c 4 -4 8.8.8.8 -q >> /dev/null
if [ "$?" -ne 0 ]; then
    sudo systemctl restart network-manager
    date +'%Y%m%d %H:%M' >> $logdir/restarts
fi
