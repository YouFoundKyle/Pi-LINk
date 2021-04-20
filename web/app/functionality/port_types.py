import json

# FUNC_PATH = "/etc/pilink/web/app/functionality/"
FUNC_PATH = "/home/kyle/code/pi-link/web/app/functionality/"
def get_port_info(port):
    with open(FUNC_PATH + "port_security.json", "r+") as prt:
        port_info = json.load(prt)
        if port in port_info["ports"].keys():
            return port_info["ports"][port]
        else:
            return {"risk": -1 , "service": "Unknown", "comment": "Unknown Port"}