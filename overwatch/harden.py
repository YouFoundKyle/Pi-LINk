from env_config import *
import iptc 
import json

info_keys = ['mac_prefixes', 'os']


def toggle_port(pmap, action, ip):
    """
    Toggles whether a port is open or closed

    Args:
        pmap (dict): dict of information needed for port
        action (str): Action to apply to the port: 'ACCEPT' || 'DENY'
        ip (str): The ip address assigned by this lease 
    """
    rule = {'protocol': pmap['protocol'], 'target': action, pmap['protocol']: {'dport': pmap['port']}, 'src': ip}
    iptc.easy.add_rule(rule)
    
    # TODO: This might be useful so gonna leave this
    # rule = iptc.Rule()
    # rule.src = ip

    # match = iptc.Match(rule, "tcp")
    # match.
    # rule.add_match(match)

    # target = iptc.Target(rule, "DROP")
    # rule.target = target

def block_external_access(device):
    """
    Block any external network access for device

    Args:
        device (dict): lease information of the device
        ip (str): ip of the device
    """
    rule = iptc.Rule()
    rule.out_interface("etho0")
    rule.src = device.ip
    rule.protocol = "tcp"
    iptc.easy.add_rule(rule)
    
def execute_action(action, action_data, device):
    """
    Take an action and route to proper function

    Args:
        action (str): action that should be taken
        action_data (dict): information needed for action
        device (Lease): lease object of the device
    """
    if action == 'static_ip':
        pass
    elif action == 'open_ports':
        for port in action_data:
            toggle_port(port, 'ACCEPT', device.ip)
    elif action == 'interent':
        if not action_data:
            block_external_access(device)
    else:
        print("Error: {a} is not a supported hardening action".format(a = action))

def read_model(model, device):
    """
    Read information from a model to decide what rules should be applied

    Args:
        model   (str):  name of preexisting 
        device  (lease): lease object of the device
    """
    try: 
        with open(SERVICE_PATH + "models/" + model) as f:
            data = json.load(f)
            for action in data.keys():
                if action not in info_keys:
                    execute_action(action, data[action], device)

    except Exception as err:
        print(f'Error applying hardening rules to device... {err}')