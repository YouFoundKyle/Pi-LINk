# Pi-LINk

## Installation 

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.org/software/).

2. Flash the SD card with Ubuntu Server 20.10.

3. Run `install_basic.sh` script.

4. Fill in `./services/mqtt2prometheus/config.yaml` and  `./services/prometheus/prometheus.yml`

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
|1883| Mosquitto  | MQTT Broker | Y
|8000| Django  | Django WebUI | Y
|8123| HomeAssistant  | HomeAssistant WebUI | Y
|9090| Prometheus | Prometheus WebUI | Y
