import analyze_leases
from env_config import *
import pickle
from datetime import datetime
import time
import json

def check_leases(path):
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
    lease_data = analyze_leases.process_lease_data(lease_list)
    json_contents = []
    for lease in lease_data:
        portscan_results = analyze_leases.scan(lease["IP"])
        scan_data = analyze_leases.process_portscan(portscan_results, lease["IP"])
        lease["port_usage"] = scan_data
        lease["date"] = datetime.now().strftime("%H_%M_%S")
        json_contents.append(lease)
    return json_contents

def get_analysis_dif (expected_leases, scanned_leases):
    devices_with_changes = [device for device in expected_leases if device not in scanned_leases]
    print(devices_with_changes)

def main(path=SERVICE_PATH + NEW_LEASES_FILE):
    scanned_leases = check_leases(path)
    analysis_path = SERVICE_PATH + ANALYZED_LEASES_PREFIX + ".json"
    expected_leases = []
    with open(analysis_path, 'rb') as f:
        expected_leases = json.load(f)
    diff = get_analysis_dif(expected_leases, scanned_leases)


if __name__ == "__main__":
    while True:
        time.sleep(86400)
        main()
