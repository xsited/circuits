#!/bin/sh

ssh -l selabs 10.0.0.134 "ps -ax | grep o.py;/home/selabs/nfv/run_o.sh status"
ssh -l selabs 10.0.0.133 "ps -ax | grep o.py;/home/selabs/nfv/run_o.sh status"
echo localhost
ps -ax | grep o.py;/home/selabs/nfv/run_o.sh status

