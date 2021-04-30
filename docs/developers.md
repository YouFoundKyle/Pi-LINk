# Developer's Guide
Pi-LINk is mean't to be a platform that anyone can build upon, including you. Below are some ways that you can add on to the Pi-LINk project.


## Adding additional hardening steps
If you want to add a new 

1. Add an option to a hardening model (just a key in a json)
2. Add a function in harden.py
3. Add line to execute_function that checks for key and call function if key exists 

## Adding hardening compatibility with a new device 
If an IoT device is not known to PI-LINk, then it will automatically have all ports and external network access blocked. In order to add compatability for a new type of device, follow the instructions below. 

Currently, Pi-LINk trys its best to determine a device type by looking at the ports it has open. 

1. Determine what unique ports the device has open
    - This can be done by running a port scanner on the device or looking up the device's documentation.

2. Navigate to `overwatch/harden.py` and look for the `get_device_type` function. Edit this function to perform a check for the specific port(s) found in step one, and have it return the name of the device type `name`
3. Navitate to `overwatch/models/` and create a new json called `name`.json . Add the desired hardening keys to the json along with its required data, look at other models as an example. 
