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
import nmap3

def check_new_lease(path):
    """
    Examines latest entry in the provided copy of the dhcpd.leases
    file. Provides information about lessee, including the MAC address,
    manufacturer (if available), port scan results, client hostname (if
    available).

    :return: the filepath of the JSON output
    """
    print("Examining new lease entries...")

    with open(path, 'rb') as f:
        lease_list = pickle.load(f)

    if not lease_list:
        print("ERROR: No Lease File Found")
        return ""

    # lease_data is a list
    lease_data = process_lease_data(lease_list)
    print(lease_data)
    json_contents = []
    for lease in lease_data:
        portscan_results = scan(lease["IP Address"])
        scan_data = process_portscan(portscan_results, lease["IP Address"])
        lease["Port Usage"] = scan_data
        lease["Analysis Date"] = datetime.now().strftime("%H_%M_%S")
        json_contents.append(lease)
    filename = SERVICE_PATH + ANALYZED_LEASES_PREFIX + ".json"
    with open(filename, "w") as fi:
        json_data = json.dumps(json_contents)
        fi.write(json_data)
    return filename, json_contents


def scan(ip_addr):
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


def process_lease_data(new_leases):
    leases = []
    for l in new_leases:
        data = {"IP Address": l.ip,
                "MAC Address": l.ethernet,
                "Lease State": l.binding_state}
        host = l.hostname
        if host:
            data["Hostname"] = host
        else:
            data["Hostname"] = "Unknown"
        data["Device Vendor"] = find_mac(data["MAC Address"])
        leases.append(data)
    return leases


def find_mac(mac_addr):
    mac_data = MacLookup()
    mac_data.update_vendors()
    try:
        return mac_data.lookup(mac_addr)
    except KeyError:
        return "Unknown"


def main(path=SERVICE_PATH + NEW_LEASES_FILE):
    result_path, new_leases = check_new_lease(path)
    if result_path:
        print("Device analysis successful - results are located in " + result_path)
    else:
        print("Error: device analysis unsuccessful. Ensure a valid lease file was provided.")
    return new_leases

if __name__ == "__main__":
    main()

