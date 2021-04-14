#! /usr/bin/env python3
import os
import json
from env_config import *
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
        print("Nothing to update: lease_info.json does not exist.\n")
    else:
        with open(source) as lf:
            new_leases = json.load(lf)
            dest = PILINK_PATH + WEB_FOLDER + LEASE_DB_PREFIX + ".json"
            if not os.path.exists(dest):
                create_leaseDB(new_leases, dest)
            else:
                modify_leaseDB(new_leases, dest)


def create_leaseDB(new_leases, dest):
    with open(dest, "w") as df:
        db = {}
        for lease in new_leases:
            mac = lease.pop("MAC")
            db[mac] = lease
        db_json = json.dumps(db)
        df.write(db_json)
        print("Created new leaseDB.json file in " + dest)


def modify_leaseDB(new_leases, dest):
    with open(dest, "r+") as df:
        data = json.load(df)
        for lease in new_leases:
            mac = lease.pop("MAC")
            data.update({mac:lease})
            print("Updated device info for MAC Address: " + mac)
        db_json = json.dumps(data)
        df.seek(0)
        df.write(db_json)
        df.truncate()


def main():
    update_leaseDB()
    # TO DO: update_lease_hist()


if __name__ == "__main__":
    main()