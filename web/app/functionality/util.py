import json
import datetime
from enum import Enum
import os.path
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

def get_alerts():
    if os.path.exists("/etc/pilink/web/alerts.json"):
        try:
            with open("/etc/pilink/web/alerts.json") as df:
                alerts = json.load(df)
                return alerts
        except ValueError:
            return []   
    else: 
        return []

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

def dump_update_info(update_info):
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "r+") as db:
        lease_db = json.load(db)
        mac = update_info['mac']
        if mac in lease_db.keys():
            print("mac is in db")
            new_date = update_info['last_update']
            lease_db[mac]["last_updated"] = new_date
            print(lease_db[mac])
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "w+") as db:
        json.dump(lease_db, db)
    print("exiting")

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
                        if 'pend_p' not in retrieved_device.keys():
                            retrieved_device['pend_p'] = []
                            retrieved_device['pend_p'].append({'port': port, 'state': 'close'})
                    else:
                        print(f"keep port {port['port_id']}")
                        selected_ports.remove(port['port_id'])
                
                # Add Requested Ports
                if selected_ports:
                    if 'pend_p' not in retrieved_device.keys():
                        retrieved_device['pend_p'] = []
                    for port in selected_ports:
                       print(f"pending port {port}")
                       retrieved_device['pend_p'].append({'port': port, 'state': 'open'})

                retrieved_device['firmware'] = device_info['firmware']
                retrieved_device['device_status'] = DeviceStatus.ENABLED.value if device_info['deviceStatus'] else DeviceStatus.DISABLED.value
                retrieved_device['vendor'] = device_info['vendor']
                retrieved_device['hostname'] = device_info['hostname']
                retrieved_device['last_updated'] = device_info['last_updated']
                print(retrieved_device)
                lease_db[lease] = retrieved_device
                updated_leases = lease_db
                break
        
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "w+") as ldb:
        json.dump(updated_leases, ldb)
