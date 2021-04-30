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
import analyze_leases
import harden
import mng_lease_DB

class EventLisenter(LoggingEventHandler):

    def dispatch(self, event):
        """
        Triggered whenever an event is registered

        Args:
            event (object): watchdog event with information about file changes
        """
        if (event.event_type == 'modified' and event.src_path == LEASES_PATH):
            print("DHCP Lease Change Detected...")
            cur_leases = self.get_current_leases()
            old_leases = self.get_old_leases()
            new_leases = []
            for lease in cur_leases:
                if self.is_new_lease(lease, old_leases, new_leases) :
                    print("New DHCP lease detected for MAC: {mac}\n".format(mac=lease['ethernet']))
                    print("{mac} details: {dets}\n".format(mac=lease['ethernet'], dets=str(lease)))
                    new_leases.append(lease)
            if len(new_leases) == 0:
                print("No new leases detected...\n")
                return
            print("Dumping {n} new leases...".format(n=len(new_leases)))
            self.dump_new_leases(new_leases)
            print("Saving current dhcp.leases to old_leases file...")
            with open(SERVICE_PATH + OLD_LEASES_FILE, "wb") as update_old:
                pickle.dump(list(cur_leases), update_old, pickle.HIGHEST_PROTOCOL)
            analyze_leases.main()
            for lease in new_leases:
                print(f"Applying Hardening to {lease['ip']}...")
                harden.read_model(lease)
            mng_lease_DB.update_leaseDB()
                

    def is_new_lease(self, lease, old, new):
        """
        Check if a lease has been seen before

        Args:
            lease (object): the lease being checked
            old (list): list of old leases saved
            new (list): list of new leases from this event trigger

        Returns:
            boolean: is a lease new or not
        """
        for old_lease in old:
            if old_lease['ethernet'] == lease['ethernet']:
                print(f"This is an old lease... {lease['ethernet']}")
                return False
        for new_lease in new:
            if new_lease['ethernet'] == lease['ethernet']:
                print(f"This is an duplicate lease... {lease['ethernet']}")
                return False
        print(f"This is an new lease... {lease['ethernet']}")
        return True

    def get_old_leases(self):
        """
        Get a list of all the leases before this event trigger

        Returns:
            list: list of old lease objects
        """
        if os.path.exists(SERVICE_PATH + OLD_LEASES_FILE):
            with open(SERVICE_PATH + OLD_LEASES_FILE, "rb") as f:
                data = pickle.load(f)
            print(f"Old Leases: {data}\n")
        else:
            data = []
            print("Old Leases: Empty.\n")
        return data
    
    def get_current_leases(self):
        """
        Get all the current leases from the dhcp leases file

        Returns:
            list: all current leases
        """
        lease_list = []
        with open(LEASES_PATH, "r+") as f:
            lease_lines = f.read().splitlines()
            for line in lease_lines:
                lease = {}
                parts = line.split(" ")
                lease['lease_end'] = parts[0]
                lease['static_ip'] = True if parts[0] == 0 else False
                lease['ethernet'] = parts[1]
                lease['ip'] = parts[2]
                lease['hostname'] = parts[3] if parts[3] != '*' else ''
                lease['client_id'] = parts[4] if parts[4] != '*' else ''
                lease_list.append(lease)
        print(f"All Current Leases: {lease_list}\n" )
        return lease_list
    
    def dump_new_leases(self, new_leases):
        """
        Save all new leases to a file

        Args:
            new_leases (list): list of new leases found during this trigger
        """
        with open(SERVICE_PATH + NEW_LEASES_FILE, 'wb') as output:
            print("Saving all new leases to new_leases file...")
            pickle.dump(new_leases, output, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = EventLisenter()
    observer = Observer()
    observer.schedule(event_handler, LEASES_PATH, recursive=True)
    observer.start()
    print("DHCP Watchdog started...")
    try:
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
