## OverWatch


## Installation

 - Requires prerequirsites
  - install with `sudo apt-get -y install python3-pip python3-virtualenv nmap`
- Create venv
    - `virtualenv venv`
- activate venv
    - `source venv/bin/activate`
- install packages
    - `pip3 install -r requirements.txt`
 

 ## Notes:
 Requires nmap be installed on system
 Requires XTABLES_LIBDIR=/usr/lib/iptables environment variable


## Files:
old_leases.pk1
   - previously captured leases from dhcp (updates after each run: gets replaced with all current leaes)
new_leases.pk1
   - list of leases that are current and not in old leases
lease_info.json
  - analyses of the new leases (ports mapping, dhcp info  (output of analyze leases))
leaseDB.json
  - DB used for web site (ever updating list of lease_info, contains any information ever captured by lease info)
  