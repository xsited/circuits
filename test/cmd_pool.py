from subprocess import Popen

commands = [
    'date; ls -l; sleep 1; date',
    'date; sleep 5; date',
    'date; df -h; sleep 3; date',
    'date; hostname; sleep 2; date',
    'date; uname -a; date',
]
# run in parallel
# processes = [Popen(cmd, shell=True) for cmd in commands]
# do other things here..
# wait for completion
# for p in processes: p.wait()


# To limit number of concurrent commands you could use multiprocessing.dummy.Pool 
# that uses threads and provides the same interface as multiprocessing.Pool that uses processes:

from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call

pool = Pool(2) # two concurrent commands at a time
for i, returncode in enumerate(pool.imap(partial(call, shell=True), commands)):
    if returncode != 0:
       print("%d command failed: %d" % (i, returncode))

