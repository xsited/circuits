#!/usr/bin/env python

"""Command line script to regularly send a ping request to 8.8.8.8
and check the response to determine network connectivity.

This program is under MIT Licence, please find the content of the license below

The MIT License (MIT)

Copyright (c) 2013 Akshet Pandey

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import argparse
import select
import signal
import socket
from time import time, sleep, ctime
from collections import deque
from datetime import timedelta

try:
    import ping
except ImportError:
    ping = None
    print 'You will need the ping python module installed to use this script'
    print 'You can install it using the following command'
    print 'pip install ping'
    sys.exit(1)

if sys.platform == "linux" or sys.platform == "linux2":
    try:
        import notify2
        notify2.init('Net Status')
    except ImportError:
        notify2 = None
elif sys.platform == "darwin":
    try:
        from pync import Notifier
    except ImportError:
        Notifier = None

try:
    import daemonize
except ImportError:
    daemonize = None

__author__ = "Akshet Pandey"
__copyright__ = "Copyright 2013, Akshet Pandey"
__license__ = "MIT"
__version__ = "1.0.0"
__date__ = "2013-08-08"
__maintainer__ = "Akshet Pandey"
__email__ = "argetlam [dot] akshet [at] gmail [dot] com"
__status__ = "Development"


def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])


def showNotification(title, body):
    if sys.platform == "linux" or sys.platform == "linux2":
        n = notify2.Notification(title, body)
        n.show()
    elif sys.platform == "darwin":
        Notifier.notify(body, title=title)


class PingLoop:
    def __init__(self, options):
        self.options = options
        self.loop = True
        signal.signal(signal.SIGINT, self.stopLoop)

    def stopLoop(self, signal, frame):
        if self.loop:
            self.loop = False
            print 'Received exit signal. Stopping!'

    def runPingLoop(self):
        delayList = deque(maxlen=100)
        lastTimeout = None
        netUp = True
        replySuccessCount = 0
        replyFailCount = 0

        cls()
        while self.loop:
            try:
                delay = ping.do_one('8.8.8.8', 3, 64)
            except socket.error:
                delay = None
            except select.error:
                delay = None

            if delay:
                delayList.append(delay)
                replySuccessCount += 1
                replyFailCount = 0
            else:
                lastTimeout = time()
                replySuccessCount = 0
                replyFailCount += 1

            if replySuccessCount >= 10 and not netUp:
                netUp = True
                if self.options.notify:
                    showNotification('Net Status', 'Net is back!')
            elif replyFailCount >= 10 and netUp:
                netUp = False
                if self.options.notify:
                    showNotification('Net Status', 'Net is down!')

            if not self.options.quite or not delay:
                cls()
                if len(delayList):
                    print 'Average delay of last ', len(delayList), ' pings is ', sum(delayList) / len(
                        delayList) * 1000, ' ms'
                if not self.options.quite and lastTimeout:
                    print 'Last timeout was ', str(timedelta(seconds=time() - lastTimeout)), 'seconds ago.'
                elif lastTimeout:
                    print 'Last timeout was at ', ctime(lastTimeout)
                else:
                    print 'There has been no timeouts yet! Hurray!'
                sleep(1)


def getRoot():
    print 'This script needs to run as root. Please provide your sudo password'
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)
    return os.getuid()


def parseOptions():
    parser = argparse.ArgumentParser(prog='check_internet.py', description='Keep a track of the internet connection')
    parser.add_argument('-q', '--quite', action='store_true',
                        help='Quite mode, update the terminal only when there is a timeout')
    parser.add_argument('-n', '--notify', action='store_true',
                        help='Notify, Send a desktop notification on disconnect/reconnect. (Only OSX)')
    parser.add_argument('-d', '--daemonize', action='store_true',
                        help='Run the process in the background as a daemon. Will automatically enable notify option')
    args = parser.parse_args()
    return args


def main():
    options = parseOptions()
    uid = os.getuid()
    if uid != 0:
        uid = getRoot()
        if uid != 0:
            print 'Failed to get root permissions. Exiting!'
            sys.exit(1)

    if options.notify or options.daemonize:
        if sys.platform == "linux" or sys.platform == "linux2" and not notify2:
            print 'You do not have the necessary library to enable notifications'
            print 'Install the library using the following command'
            print 'pip install notify2'
            sys.exit(1)
        elif sys.platform == "darwin" and not Notifier:
            print 'You do not have the necessary library to enable notifications'
            print 'Install the library using the following command'
            print 'pip install pync'
            sys.exit(1)

    if options.daemonize and not daemonize:
        print 'You do not have the necessary library run in daemon mode'
        print 'Install the library using the following command'
        print 'pip install daemonize'
        sys.exit(1)

    if options.daemonize:
        options.notify = True
        pingLoop = PingLoop(options)
        daemon = daemonize.Daemonize(app='check_network', pid='/tmp/check_network.pid', action=pingLoop.runPingLoop)
        daemon.start()
    else:
        if options.quite:
            print('Running in quite mode, will update when a timeout occurs')

        pingLoop = PingLoop(options)
        pingLoop.runPingLoop()


if __name__ == '__main__':
    main()
