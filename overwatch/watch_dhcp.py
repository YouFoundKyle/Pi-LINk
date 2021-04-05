#! /usr/bin/env python3
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import json
import pickle
from isc_dhcp_leases import Lease, IscDhcpLeases
from env_config import *
import os.path
import analyze_lease

#TODO: Dont get All leases all the time 
class EventLisenter(LoggingEventHandler):

    def dispatch(self, event):
        print("Change Detected: type: {e} path: {p}".format(e=event.event_type, p = event.src_path))
        if (event.event_type == 'modified' and event.src_path == '/var/lib/dhcp/dhcpd.leases'):
            print("DHCP Lease Change Detected...\n")
            cur_leases = self.get_current_leases()
            old_leases = self.get_old_leases()
            new_leases = []
            for lease in cur_leases:
                if lease not in old_leases:
                    print("New DHCP lease detected for MAC: {mac}\n".format(mac=lease.ethernet))
                    print("{mac} details: {dets}\n".format(mac=lease.ethernet, dets=str(lease)))
                    new_leases.append(lease)
            if len(new_leases) > 0:
                print("Dumping {n} new leases...\n".format(n=len(new_leases)))
                self.dump_new_leases(new_leases)
                analyze_lease.main()
                with open(SERVICE_PATH + OLD_LEASES_FILE, "wb") as update_old:
                    pickle.dump(cur_leases, update_old, pickle.HIGHEST_PROTOCOL)
            else:
                print("No new leases detected...\n")


    def get_old_leases(self):
        if os.path.exists(SERVICE_PATH + OLD_LEASES_FILE):
            with open(SERVICE_PATH + OLD_LEASES_FILE, "rb") as f:
                data = pickle.load(f)
            print("Old Leases: {oldlease}\n".format(oldlease=data))
        else:
            data = []
            print("Old Leases: Empty.\n")
        return data
    
    def get_current_leases(self):
        leases = IscDhcpLeases(LEASES_PATH)
        all_leases = leases.get()
        current_leases = leases.get_current()
        print("All Leases: {all}\n".format(all=all_leases) )
        print("Current Leases: {curr}\n".format(curr=current_leases) )
        return all_leases
    
    def dump_new_leases(self, new_leases):
        with open(SERVICE_PATH + NEW_LEASES_FILE, 'wb') as output:
            pickle.dump(new_leases, output, pickle.HIGHEST_PROTOCOL)

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