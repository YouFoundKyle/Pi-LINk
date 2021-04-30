#! /usr/bin/env python3
import os
import json
from env_config import *
from datetime import date
from shutil import copyfile
"""
This module collects data on new leases from "lease_info.json" and 
updates the "leaseDB.json" file, which contains current and
up to date information about active leases to display on the
"device overview" dashboard.

TO DO: Functionality to remove leases that are nonexistent.
"""

# leaseDB.json is a dictionary where keys are MAC addresses
def update_leaseDB():
    source = PILINK_PATH + OVERWATCH_FOLDER + ANALYZED_LEASES_PREFIX + ".json"
    if not os.path.exists(source):
        print("Nothing to update: lease_info.json does not exist.")
    else:
        with open(source) as lf:
            new_leases = json.load(lf)
            dest = PILINK_PATH + WEB_FOLDER + LEASE_DB_PREFIX + ".json"
            if not os.path.exists(dest):
                create_leaseDB(new_leases, dest)
            else:
                modify_leaseDB(new_leases, dest)

def copy_DB():
    source = LEASE_DB_PATH
    dest = SERVICE_PATH + "copy_DB.json"
    if not os.path.exists(source):
        print("Nothing to update: lease_DB.json does not exist.")
    else:
        with open(source, "r") as orig, open(dest, "w") as copy:
            orig_contents = json.load(orig)
            copy_contents = json.dumps(orig_contents)
            copy.write(copy_contents)
            print("Copied lease_DB.json file to " + dest)

def create_leaseDB(new_leases, dest):
    with open(dest, "w") as df:
        db = {}
        print("Created new leaseDB.json file in " + dest)
        for lease in new_leases:
            mac = lease.pop("MAC")
            lease["last_updated"] = date.today().strftime("%m/%d/%y")
            lease["firmware"] = "Unknown"
            # lease["device_status"] = "Enabled"
            db[mac] = lease
            print("Saved device info for MAC Address " + mac + " in " + dest)
        db_json = json.dumps(db)
        df.write(db_json)


def modify_leaseDB(new_leases, dest):
    with open(dest, "r+") as df:
        data = json.load(df)
        for lease in new_leases:
            mac = lease.pop("MAC")
            data[mac].update(lease)
            print("Updated device info for MAC Address: " + mac + " in " + dest)
        db_json = json.dumps(data)
        df.seek(0)
        df.write(db_json)
        df.truncate()


def main():
    update_leaseDB()

if __name__ == "__main__":
    main()