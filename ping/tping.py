#!/usr/bin/env python
from threading import Thread
import subprocess
from Queue import Queue
import re

matcher = re.compile("round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
num_threads = 5
queue = Queue()
ips = ["google.com", "yahoo.com", "amazon.com", "10.0.1.11", "10.0.1.51"]
#wraps system ping command
def pinger(i, q):
    """Pings subnet"""
    while True:
        ip = q.get()
        print "\nThread %s: Pinging %s" % (i, ip)
	ping = subprocess.Popen(
    		["ping", "-c", "4", ip],
    		stdout = subprocess.PIPE,
    		stderr = subprocess.PIPE
	)

	out, error = ping.communicate()
       # ret = subprocess.call("ping -c 1 %s" % ip,
       #     shell=True,
       #     stdout=open('/dev/null', 'w'),
       #     stderr=subprocess.STDOUT)
          #  stderr=open('/dev/null', 'w'))
           # stdout=subprocess.STDOUT,
        if ret == 0:
            print "%s: is alive" % ip
	    print matcher.match(stderr).groups()
        else:
            print "%s: did not respond" % ip
        q.task_done()
#Spawn thread pool
for i in range(num_threads):

    worker = Thread(target=pinger, args=(i, queue))
    worker.setDaemon(True)
    worker.start()
#Place work in queue
for ip in ips:
    queue.put(ip)
#Wait until worker threads are done to exit    
queue.join()
