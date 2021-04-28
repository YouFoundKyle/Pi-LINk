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
from datetime import date
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
        portscan_results = scan(lease["IP"])
        scan_data = process_portscan(portscan_results, lease["IP"])
        lease["port_usage"] = scan_data
        lease["date_added"] = date.today().strftime("%m/%d/%y")
        json_contents.append(lease)
    filename = SERVICE_PATH + ANALYZED_LEASES_PREFIX + ".json"
    with open(filename, "w") as fi:
        json_data = json.dumps(json_contents)
        fi.write(json_data)
    return filename, json_contents


def scan(ip_addr):
    nmap = nmap3.NmapHostDiscovery()
    results = nmap.nmap_portscan_only(ip_addr)
    print(f"nmap results: {results}")
    return results


def process_portscan(portscan_results, ip_addr):
    ports = portscan_results[ip_addr]["ports"]
    results = []
    for port in ports:
        port_dict = {"port_id": port["portid"],
                     "protocol": port["protocol"],
                     "port_state": port["state"],
                     "service": port["service"]["name"]}
        results.append(port_dict)
    return results


def process_lease_data(new_leases):
    leases = []
    for l in new_leases:
        data = {"IP": l.['ip'],
                "MAC": l.['ethernet'],
                "lease_state": l.['binding_state'],
                "static_ip": l['static_ip']}
        host = l.['hostname']
        if host:
            data["hostname"] = host
        else:
            data["hostname"] = "Unknown"
        data["vendor"] = find_mac(data["MAC"])
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

