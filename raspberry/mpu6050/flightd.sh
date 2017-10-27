#!/bin/bash
# /etc/init.d/flightd

### BEGIN INIT INFO
# Provides:          flightd
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Flight Monitor"
# Description:       This service is used to log MPU6050
### END INIT INFO


case "$1" in 
    start)
        echo "Starting Flight Monitor"
        python /usr/local/src/flightmonitor/service.py start
        ;;
    stop)
        echo "Stopping Flight Monitor"
        python /usr/local/src/flightmonitor/service.py stop
        ;;
    *)
        echo "Usage: /etc/init.d/flightd start|stop"
        exit 1
        ;;
esac

exit 0
