#! /usr/bin/env python3
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import json
from isc_dhcp_leases import Lease, IscDhcpLeases


PILINK_PATH='/etc/pilink'
LEASES_PATH= '/var/lib/dhcp/dhcpd.leases'
class EventLisenter(LoggingEventHandler):

   
    def dispatch(self, event):
        print("Change Detected: type: {e} path: {p}".format(e=event.event_type, p = event.src_path))
        if (event.event_type == 'modified' and event.src_path == '/var/lib/dhcp/dhcpd.leases'):
            print('DHCP Lease Change Detected...')
            # old_leases = self.get_old_leases()
            self.get_current_leases()

    def get_old_leases(self):
        with open(PILINK_PATH + '/overwatch/leases.db') as f:
            data = json.load(f)
        print('Old Leases' + data)
        return data
    
    def get_current_leases(self):
        leases = IscDhcpLeases(LEASES_PATH)
        all_leases = leases.get()
        current_leases = leases.get_current()
        print("All Leases: {all}".format(all=all_leases) )
        print("Current Leases: {curr}".format(curr=current_leases) )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = EventLisenter()
    observer = Observer()
    observer.schedule(event_handler, LEASES_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()