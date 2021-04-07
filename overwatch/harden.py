from env_config import *
import iptc 
import json

info_keys = ['mac_prefixes', 'os']


def deny_port(pmap):
    rule = {'protocol': pmap['protocol'], 'target': 'DENY', pmap['protocol']: {'dport': pmap['port']}}
    iptc.easy.add_rule(rule)

def allow_port(pmap):
    rule = {'protocol': pmap['protocol'], 'target': 'ACCEPT', pmap['protocol']: {'dport': pmap['port']}}
    iptc.easy.add_rule(rule)

def block_external_access(device):
    rule = {}
    iptc.easy.add_rule(rule)
    
def execute_action(action, action_data):
    if action == 'static_ip':
        pass
    elif action == 'open_ports':
        for port in action_data:
            allow_port(port)
    elif action == 'interent':
        pass
    else:
        print("Error: {a} is not a supported hardening action".format(a = action))

def read_model(model):
    try: 
        with open(SERVICE_PATH + "models/" + model) as f:
            data = json.load(f)
            for action in data.keys():
                if action not in info_keys:
                    execute_action(action, data[action])

    except Exception as e:
        print("Error applying hardening rules to device... {ex}".format(ex = e))