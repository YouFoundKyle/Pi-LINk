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
import harden

class EventLisenter(LoggingEventHandler):

    def dispatch(self, event):
        """
        Triggered whenever an event is registered

        Args:
            event (object): watchdog event with information about file changes
        """
        if (event.event_type == 'modified' and event.src_path == '/var/lib/dhcp/dhcpd.leases'):
            print("DHCP Lease Change Detected...")
            cur_leases = self.get_current_leases()
            old_leases = self.get_old_leases()
            new_leases = []
            for lease in cur_leases:
                if self.is_new_lease(lease, old_leases, new_leases) :
                    print("New DHCP lease detected for MAC: {mac}\n".format(mac=lease.ethernet))
                    print("{mac} details: {dets}\n".format(mac=lease.ethernet, dets=str(lease)))
                    new_leases.append(lease)
            if len(new_leases) == 0:
                print("No new leases detected...\n")
                return

            print("Dumping {n} new leases...".format(n=len(new_leases)))
            self.dump_new_leases(new_leases)
            print("Saving old leases to file...")
            with open(SERVICE_PATH + OLD_LEASES_FILE, "wb") as update_old:
                pickle.dump(cur_leases, update_old, pickle.HIGHEST_PROTOCOL)
            new_leases = analyze_lease.main()
            for lease in new_leases:
                print(f"Applying Hardening to {lease.ip}...")
                harden.read_model('standard', lease)
                

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
            if old_lease.ethernet == lease.ethernet:
                return False
        for new_lease in new:
            if new_lease.ethernet == lease.ethernet:
                return False
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
            print("Old Leases: {oldlease}\n".format(oldlease=data))
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
        leases = IscDhcpLeases(LEASES_PATH)
        all_leases = leases.get()
        current_leases = leases.get_current()
        print("All Leases: {all}\n".format(all=all_leases) )
        print("Current Leases: {curr}\n".format(curr=current_leases) )
        return current_leases
    
    def dump_new_leases(self, new_leases):
        """
        Save all new leases to a file

        Args:
            new_leases (list): list of new leases found during this trigger
        """
        with open(SERVICE_PATH + NEW_LEASES_FILE, 'wb') as output:
            print("Saving new leases to file...")
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
