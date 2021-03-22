#! /usr/bin/env python3
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class EventLisenter(LoggingEventHandler):
    def dispatch(self, event):
        print("Change Detected: {e}".format(e=event))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    path = '/var/lib/dhcp/dhcpd.leases'
    event_handler = EventLisenter()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()