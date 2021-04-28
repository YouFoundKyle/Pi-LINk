import json
import datetime
from enum import Enum
ROOT_DIR = "/etc/pilink"
FUNC_PATH = "/web/app/functionality/"
OVERWATCH_PATH = "/overwatch/"
class DeviceStatus(Enum):
    ENABLED = "Enabled"
    DISABLED = "Disabled"

def get_port_info(port):
    """
    Returns information about a specific port and its risk levels
    """
    with open(ROOT_DIR + FUNC_PATH + "port_security.json", "r+") as prt:
        port_info = json.load(prt)
        if port in port_info["ports"].keys():
            return port_info["ports"][port]
        else:
            return {"risk": -1 , "service": "Unknown", "comment": "Unknown Port"}

def get_port_list (port_info):
    ports = []
    for p in port_info:
        if p['port_state'] == "open":
            ports.append(p["port_id"])
    return ports

def get_device_info(ip):
    """
    Returns all information saved about a specific device
    """
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "r+") as lif:
        lease_info = json.load(lif)
        for mac in lease_info.keys():
            lease = lease_info[mac]
            if lease["IP"] == ip:
                lease['port_list'] = get_port_list(lease['port_usage'])
                lease['MAC'] = mac
                return lease
    return {"IP":ip,"MAC":"NOT FOUND", "lease_state":"NOT FOUND", "hostname":"NOT FOUND", "vendor":"NOT FOUND","port_usage":[],"date":"NOT FOUND", "unknown": None}


def dump_device_info(device_info):
    """
    Returns all information saved about a specific device to the lease_info db
    """
    updated_leases = {}
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "r+") as ldb:
        lease_db = json.load(ldb)
        for lease in lease_db.keys():
            if lease == device_info['mac']:
                retrieved_device = lease_db[lease]
                used_ports = retrieved_device['port_usage']
                selected_ports = device_info['ports'].split(' ')
                # Remove requested ports
                for port in used_ports:
                    if port['port_id'] not in selected_ports:
                        print(f"remove port {port['port_id']} not in {selected_ports}")
                        used_ports.remove(port)
                    else:
                        print(f"keep port {port['port_id']}")
                    selected_ports.remove(port['port_id'])
                
                # Add Requested Ports
                if selected_ports:
                    if 'pend_p' not in retrieved_device.keys():
                        retrieved_device['pend_p'] = []
                    for port in selected_ports:
                       print(f"pending port {port}")
                       retrieved_device['pend_p'].append(port)

                retrieved_device['last_updated'] = datetime.date.today().strftime("%m/%d/%y")
                retrieved_device['firmware'] = device_info['firmware']
                retrieved_device['device_status'] = DeviceStatus.ENABLED.value if device_info['deviceStatus'] else DeviceStatus.DISABLED.value
                retrieved_device['vendor'] = device_info['vendor']
                retrieved_device['hostname'] = device_info['hostname']
                print(retrieved_device)
                updated_leases = lease_db
                break
        
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "w+") as ldb:
        json.dump(updated_leases, ldb)