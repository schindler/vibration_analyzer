# -*- coding: utf-8 -*-
"""
    Service to read data from Sensor and save
    sudo apt-get install python-daemon
"""

import data
import mpu6050

from daemon import runner

class FlightMonitor(object):
    """FlightMonitor Service."""

    def __init__(self):
        """Initialize Daemon."""
        self.stdin_path = '/dev/null'
        self.stdout_path = '/tmp/flight_monitor_stdout.txt'
        self.stderr_path = '/tmp/flight_monitor_stderr.txt'
        self.pidfile_path = '/tmp/flight_monitor.pid'
        self.pidfile_timeout = 1

    def run(self):
        """Main"""
        store = data.Store()
        sensor = mpu6050.Sensor()

        while True:
            for _ in xrange(0, 1000):
                store.add(sensor.data())
            store.commit()

if __name__ == "__main__":
    runner.DaemonRunner(FlightMonitor()).do_action()
