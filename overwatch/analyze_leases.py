#! /usr/bin/env python3

"""
This module will analyze a provided copy of a dhcpd.leases file.
It is important that a copy of the dhcpd.leases file is created
immediately after detection of an update or new lease.
"""
from mac_vendor_lookup import MacLookup
import sys
import json
from env_config import *
from datetime import datetime
import pickle
import os

def check_new_lease(path):
    """
    Examines latest entry in the provided copy of the dhcpd.leases
    file. Provides information about lessee, including the MAC address,
    manufacturer (if available), port scan results, client hostname (if
    available).

    :return: the filepath of the JSON output
    """
    with open(path, 'rb') as f:
        lease_list = pickle.load(f)

    if not lease_list:
        return ""

    # lease_data is a list
    lease_data = process_lease_data(lease_list)
    dev_analysis = []
    for lease in lease_data:
        portscan_results = scan(lease["IP Address"])
        scan_data = process_portscan(portscan_results, lease["IP Address"])
        lease["Port Usage"] = scan_data
        lease["Analysis Date"] = datetime.now().strftime("%H_%M_%S")
        dev_analysis.append(lease)
    filename = SERVICE_PATH + ANALYZED_LEASES_PREFIX + ".json"
    with open(filename, "w") as fi:
        json_data = json.dumps(dev_analysis)
        fi.write(json_data)
    return filename


def scan(ip_addr):
    import nmap3
    nmap = nmap3.NmapHostDiscovery()
    results = nmap.nmap_portscan_only(ip_addr)
    return results


def process_portscan(portscan_results, ip_addr):
    ports = portscan_results[ip_addr]["ports"]
    results = []
    for port in ports:
        port_dict = {"Port ID": port["portid"],
                     "Protocol": port["protocol"],
                     "State": port["state"],
                     "Service": port["service"]["name"]}
        results.append(port_dict)
    return results


def process_lease_data(lease_list):
    # new_lease = lease_list[-1]
    results = []
    for lease in lease_list:
        data = {"IP Address": lease.ip,
                "MAC Address": lease.ethernet,
                "Lease State": lease.binding_state}
        host = lease.hostname
        if host:
            data["Hostname"] = host
        else:
            data["Hostname"] = "Not provided."
        data["Device Vendor"] = find_mac(data["MAC Address"])
        results.append(data)
    return results


def find_mac(mac_addr):
    mac_data = MacLookup()
    mac_data.update_vendors()
    try:
        return mac_data.lookup(mac_addr)
    except KeyError:
        return "Not found."


def main(path=SERVICE_PATH + NEW_LEASES_FILE):
    result_path = check_new_lease(path)
    if result_path:
        print("Device analysis successful - results are located in " + result_path)
    else:
        print("Error: device analysis unsuccessful. Ensure a valid lease file was provided.")


if __name__ == "__main__":
    main()

