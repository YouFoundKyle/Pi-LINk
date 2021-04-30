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
        # takes care of hostname, enabled, and pend
        if (event.event_type == 'modified' and event.src_path == LEASE_DB_PATH):
            print("Lease DB Change Detected...")
            with open(LEASE_DB_PATH, "r") as db:
                lease_db =  json.load(db)
                for key in lease_db.keys():
                    lease = lease_db[key]
                    if "pend_p" in lease.keys():
                        pend_ports = lease["pend_p"]
                        for port in pend_ports:
                            # needs portmap, string 'ACCEPT' or 'DENY' and ip
                            ip = lease["IP"]
                            if port["state"] =="open"
                                port["protocol"] = ""
                                harden.toggle_port(port, 'ACCEPT', ip)
                            else:
                                harden.toggle_port(port, 'DENY', ip)
                    # pass in device dict with lowercase 'ip' as key so harden can read
                    if lease["device_status"] == "Enabled":
                        ip = lease.pop("IP")
                        lease["ip"] = ip
                        harden.read_model(lease, True)
                    else:
                        ip = lease.pop("IP")
                        lease["ip"] = ip
                        harden.read_model(lease)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = EventLisenter()
    observer = Observer()
    observer.schedule(event_handler, LEASE_DB_PATH, recursive=True)
    observer.start()
    print("LeaseDB Watchdog started...")
    try:
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()