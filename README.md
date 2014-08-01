nfv
===

nfv prototyping

post flash install
===================

yum install openssh-server
yum install openvswitch
    
service enable openssh-server
service start openssh-server
 

/sbin/service  openvswitch enable
/sbin/service  openvswitch start
/bin/systemctl enable openvswitch.service

ovs-vsctl show

Network setup for host 135
==========================


ifconfig eth0 down
ifconfig eth0 10.36.0.135 up
ip route add default dev eth0 via 10.36.0.1

ifconfig eth1 10.0.0.135 up

ifconfig isolated0 192.168.222.135 up

ifconfig eth2 0.0.0.0 up




Don't do this!
==============
 
ovs-vsctl set-controller isolated0 tcp:10.0.0.192:6633

ovs-vsctl show

Python setup

yum install python-pip

or

apt-get install python-pip


Running o.py
============

The script will tell you what is missing. but here are the requirements:


pip install Flask

pip install Flask-HTTPAuth

pip install ping

pip install daemonize

Running as root
===============

Run as root.  Not ideal, but since once script for both compute and orchestrator 
raw sockets and firing scripts require priviledge.

This works so long as you monitor the session.  You leave the service quits.


sudo python o.py

This works better. You leave it runs, but stop does not work.  Search the process table and kill.


sudo ./run_o.sh start


