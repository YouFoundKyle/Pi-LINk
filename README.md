# Pi-LINk

## Installation 

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.org/software/).

2. Flash the SD card with Ubuntu Server 20.10.

3. Run `install_basic.sh` script.

## SSH for Internet Connection Sharing (ICS) Users
1. Make sure your SD card has an "ssh" file in the boot partition.
2. Connect your laptop to your Pi using a network cable and set up ICS.
2. Open "Network Connections" from PC and identify the IPV4 address of the ethernet adapter connected to your PC.
3. Run `nmap -sn XXX.XXX.XXX.0/24` using the IP address you identified in the previous step after replacing the last part of the address with 0. This will provide the IP to SSH into your RPi Ubuntu Server. 
4. SSH into the ubuntu server.


## Wireless Network
Running a playbook turns the Raspberry Pi 4 into a wireless access point (WAP). The WAP uses 802.11g (2.4Ghz) standard and runs on channel 7 (2.442 Mhz) with more configuration options being located at `/etc/hostapd/hostapd.conf`. 
SSID: pi_network
Password: ThisIsAPi4

## Repo Structure
 - `/bin` : Includes Any scripts
 - `/configs` : Includes all config files. Loosesly mirrors setup of `/etc/`
 - `/playbooks` : Includes any playbooks needed to configure services
 - `/services/` : Includes any files required to get services running  



## Ports Used
|Port|Service|Description | External
|---|---|---|---|
|53| DNS  | DNS Server endpoint | N
