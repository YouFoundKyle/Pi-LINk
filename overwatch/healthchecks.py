import analyze_leases
from env_config import *
import pickle
from datetime import date, datetime
import time
import json

def get_warning(ip):
    return {"ip": ip , "timestamp": date.today().strftime("%m/%d/%y"), "message": f"Changes have been made to {ip}. Please check the device page."}

def post_changes(ips):
    """
    If any changes were detected, post alerts
    """
    ip_alerts = []
    for ip in ips:
        ip_alerts.append(get_warning(ip))
    with open(WARNING_PATH, 'r+') as f:
        warnings = json.load(f)
        new_warnings = warnings +ip_alerts
        print(new_warnings)
        warning_data = json.dumps(new_warnings)
        f.seek(0)
        f.write(warning_data)
        f.truncate()
    
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
        if lease["IP"] in portscan_results.keys() :
            scan_data = process_portscan(portscan_results, lease["IP"])
            lease["port_usage"] = scan_data
        else:
            lease['lease_state'] = 'inactive'
            lease["port_usage"] = []
        lease["date"] = datetime.now().strftime("%H_%M_%S")
        json_contents.append(lease)
    return json_contents

def get_analysis_dif (expected_leases, scanned_leases):
    devices_with_changes = [device for device in expected_leases if device not in scanned_leases]
    ips = []
    for device in devices_with_changes:
        ips.append(device['IP'])
    return ips

def main(path=SERVICE_PATH + NEW_LEASES_FILE):
    scanned_leases = check_leases(path)
    analysis_path = SERVICE_PATH + ANALYZED_LEASES_PREFIX + ".json"
    expected_leases = []
    with open(analysis_path, 'rb') as f:
        expected_leases = json.load(f)
    diff = get_analysis_dif(expected_leases, scanned_leases)
    post_changes(diff)

if __name__ == "__main__":
    while True:
        time.sleep(86400)
        main()
