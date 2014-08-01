nfv
===

nfv prototyping

yum install python-pip

or

apt-get install python-pip

The script will tell you what is missing. but here are the requirements:

pip install Flask
pip install Flask-HTTPAuth
pip install ping
pip install daemonize


Run as root.  Not ideal, but since once script for both compute and orchestrator 
raw sockets and firing scripts require priviledge.

This works so long as you monitor the session.  You leave the service quits.
sudo python o.py

This works better. You leave it runs, but stop does not work.  Search the process table and kill.
sudo ./run_o.sh start


