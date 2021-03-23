"""
This module will analyze a provided copy of a dhcpd.leases file.
It is important that a copy of the dhcpd.leases file is created
immediately after detection of an update or new lease.
"""
from isc_dhcp_leases import IscDhcpLeases
from mac_vendor_lookup import MacLookup
import sys

def check_new_lease(path):
    """
    Examines latest entry in the provided copy of the dhcpd.leases
    file. Provides information about lessee, including the MAC address,
    manufacturer (if available), port scan results, client hostname (if
    available), start time of lease,

    :return:
    """
    leases = IscDhcpLeases(path)
    lease_list = leases.get()

    if not lease_list:
        """ Need to raise error or exception """
        return

    lease_data = process_lease_data(lease_list)
    scan_data = scan(lease_data["IP Address"])

    fi = open("/home/ubuntu/lease_info.txt", "a")
    for key in lease_data:
        fi.write(key + ": " + lease_data[key] + "\n")
    print(scan_data)
    fi.write(scan_data + "\n")
    fi.close()

    return 0


def scan(ip_addr):
    import nmap3
    # scan_data = []
    nmap = nmap3.NmapHostDiscovery()
    results = nmap.nmap_portscan_only(ip_addr)

    return results


def process_lease_data(lease_list):
    new_lease = lease_list[-1]
    data = {"IP Address" : new_lease.ip,
            "MAC Address" : new_lease.ethernet, 
            "Lease State" : new_lease.binding_state}

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
    path = sys.argv[1]
    check_new_lease(path)

if __name__ == "__main__":
    main()
