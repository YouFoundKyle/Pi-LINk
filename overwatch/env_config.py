PILINK_PATH='/etc/pilink'
OVERWATCH_FOLDER='/overwatch/'
WEB_FOLDER='/web/'
SERVICE_PATH= PILINK_PATH + OVERWATCH_FOLDER
# LEASES_PATH= '/var/lib/dhcp/dhcpd.leases'
LEASES_PATH= '/var/lib/misc/dnsmasq.leases'
NEW_LEASES_FILE='new_leases.pkl'
OLD_LEASES_FILE='old_leases.pk1'
ANALYZED_LEASES_PREFIX='lease_info'
LEASE_DB_PREFIX='lease_DB'

## Risk Levels
LOW_RISK=1
MED_RISK=2
HIGH_RISK=3