import json
ROOT_DIR = "/etc/pilink"
FUNC_PATH = "/web/app/functionality/"
OVERWATCH_PATH = "/overwatch/"
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
    with open(ROOT_DIR + OVERWATCH_PATH + "lease_info.json", "r+") as lif:
        lease_info = json.load(lif)
        for lease in lease_info:
            if lease["IP"] == ip:
                lease['port_list'] = get_port_list(lease['port_usage'])
                return lease
    return {"IP":ip,"MAC":"NOT FOUND", "lease_state":"NOT FOUND", "hostname":"NOT FOUND", "vendor":"NOT FOUND","port_usage":[],"date":"NOT FOUND", "unknown": None}


def dump_device_info(ip, device_info):
    """
    Returns all information saved about a specific device to the lease_info db
    """
    with open(ROOT_DIR + "/web/" + "lease_DB.json", "r+") as ldb:
        lease_db = json.load(ldb)
        for lease in lease_db.keys():
            if lease == lease_db['staticMAC']:
                
                return lease
    return {"IP":ip,"MAC":"NOT FOUND", "lease_state":"NOT FOUND", "hostname":"NOT FOUND", "vendor":"NOT FOUND","port_usage":[],"date":"NOT FOUND", "unknown": None}