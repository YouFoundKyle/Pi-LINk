## SSH for Internet Connection Sharing (ICS) Users
1. Make sure your SD card has an "ssh" file in the boot partition.
2. Connect your laptop to your Pi using a network cable and set up ICS.
2. Open "Network Connections" from PC and identify the IPV4 address of the ethernet adapter connected to your PC.
3. Run `nmap -sn XXX.XXX.XXX.0/24` using the IP address you identified in the previous step after replacing the last part of the address with 0. This will provide the IP to SSH into your RPi Ubuntu Server.
4. SSH into the ubuntu server.
