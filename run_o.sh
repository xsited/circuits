#!/bin/sh

    ### BEGIN INIT INFO
    # Provides: myscript
    # Required-Start: $remote_fs $syslog
    # Required-Stop: $remote_fs $syslog
    # Default-Start: 2 3 4 5
    # Default-Stop: 0 1 6
    # Short-Description: Media remote for Pi
    # Description: Interact with program via phone
    ### END INIT INFO

    # Change the next 3 lines to suit where you install your script and what you want to call it
    DIR=/home/selabs/git/nfv
    DAEMON=$DIR/o.py
    DAEMON_NAME=o

    # This next line determines what user the script runs as.
    DAEMON_USER=selabs

    # The process ID of the script when it runs is stored here:
    PIDFILE=/var/run/$DAEMON_NAME.pid

    . /lib/lsb/init-functions

    do_start () {
            log_daemon_msg "Starting system $DAEMON_NAME daemon"
            start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --startas $DAEMON
            log_end_msg $?
    }
    do_stop () {
            log_daemon_msg "Stopping system $DAEMON_NAME daemon"
            start-stop-daemon --stop --pidfile $PIDFILE --retry 10
            log_end_msg $?
    }

    case "$1" in
            start|stop)
                    do_${1}
                    ;;

            restart|reload|force-reload)
                    do_stop
                    do_start
                    ;;

            status)
                    status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
                    ;;
            *)

            echo "Usage: /etc/init.d/$DEAMON_NAME {start|stop|restart|status}"
            exit 1
            ;;
    esac
    exit

