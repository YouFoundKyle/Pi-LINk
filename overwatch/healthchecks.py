import analyze_leases
from env_config import *
import pickle
import datetime
import time

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

def get_analysis_dif (current, checked):
    missing_in_current_but_in_checked = checked.keys() - current
    devices_with_changes = [device for device in current if device not in checked]


def main(path=SERVICE_PATH + NEW_LEASES_FILE):
    lease_check = check_leases(path)
    analysis_path = SERVICE_PATH + ANALYZED_LEASES_PREFIX + ".json"
    current_devices = []
    with open(analysis_path, 'rb') as f:
        prev_analysis = pickle.load(f)
        current_devices = prev_analysis['Device Info']
    diff = get_analysis_dif(current_devices, lease_check)

    

    

if __name__ == "__main__":
    while True:
        time.sleep(86400)
        main()
