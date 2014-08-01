#!/bin/bash
 
SERVER="192.168.200.11"
LOG="client-iperf.log"
TIME="5"
 
 
if [ "$1" == "-v" ]; then
        iperf -t $TIME -c $SERVER -r -p 5005 -y C | tee -a $LOG
else
        iperf -t $TIME -c $SERVER -r -p 5005 -y C >> $LOG
fi
