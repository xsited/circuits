#!/usr/bin/env python

# Import the module
import subprocess
import iperf

# Ask the user for input
#host = raw_input("Enter a host to ping: ")	

#print iperf.BuildClientCommand(host)

# Set up the echo command and direct the output to a pipe
p1 = subprocess.Popen(['iperf', '-t 15', '-u', '-c',  '127.0.0.1'], stdout=subprocess.PIPE)

# Run the command
output = p1.communicate()[0]

#print output
iperf.ParseIperfOutput(output)
#print iperf._ParseUdpOutput(output[2])
