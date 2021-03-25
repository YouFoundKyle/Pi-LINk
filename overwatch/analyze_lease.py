"""
This module will analyze a provided copy of a dhcpd.leases file.
It is important that a copy of the dhcpd.leases file is created
immediately after detection of an update or new lease.
"""
from isc_dhcp_leases import IscDhcpLeases
from mac_vendor_lookup import MacLookup
import sys
import json
from datetime import datetime
from env_config import *
import pickle

def check_new_lease(path):
    """
    Examines latest entry in the provided copy of the dhcpd.leases
    file. Provides information about lessee, including the MAC address,
    manufacturer (if available), port scan results, client hostname (if
    available), start time of lease,

    :return:
    """
    with open(path) as f:
            lease_list = pickle.load(f)

    if not lease_list:
        return ""

    lease_data = process_lease_data(lease_list)
    portscan_results = scan(lease_data["IP Address"])
    scan_data = process_portscan(portscan_results, lease_data["IP Address"])
    file_contents = {"Device Info": lease_data, "Port Usage": scan_data}
    filename = SERVICE_PATH + ANALYZED_LEASES_PREFIX + datetime.now().strftime("%I_%M_%S") + ".json"
    fi = open(filename, "a")

    json_data = json.dumps(file_contents)
    fi.write(json_data + "\n")
    fi.close()
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
    new_lease = lease_list[-1]
    data = {"IP Address": new_lease.ip,
            "MAC Address": new_lease.ethernet,
            "Lease State": new_lease.binding_state}
    host = new_lease.hostname
    if host:
        data["Hostname"] = host
    else:
        data["Hostname"] = "Not provided."
    data["Device Vendor"] = find_mac(data["MAC Address"])
    return data


def find_mac(mac_addr):
    mac_data = MacLookup()
    mac_data.update_vendors()
    try:
        return mac_data.lookup(mac_addr)
    except KeyError:
        return "Not found."


def main():
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        results = check_new_lease(path)
    else:
        print("Using default new lease filepath")
        results = check_new_lease(NEW_LEASES_FILE)
    if results:
        print("Device analysis successful - results are located in " + results)
    else:
        print("Error: device analysis unsuccessful. Ensure a valid lease file was provided.")


if __name__ == "__main__":
    main()

