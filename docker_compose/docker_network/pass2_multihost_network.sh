


# https://goldmann.pl/blog/2014/01/21/connecting-docker-containers-on-multiple-hosts/

ASUS_IP=192.168.1.12
STAR_IP=192.168.1.167


# The 'other' host
REMOTE_IP=$STAR_IP


# Name of the bridge
BRIDGE_NAME=docker0
# Bridge address
BRIDGE_ADDRESS=172.17.0.1/16

# Deactivate the docker0 bridge
ip link set $BRIDGE_NAME down
# Remove the docker0 bridge
brctl delbr $BRIDGE_NAME
# Delete the Open vSwitch bridge
ovs-vsctl del-br br0
# Add the docker0 bridge
brctl addbr $BRIDGE_NAME
# Set up the IP for the docker0 bridge
ip a add $BRIDGE_ADDRESS dev $BRIDGE_NAME
# Activate the bridge
ip link set $BRIDGE_NAME up
# Add the br0 Open vSwitch bridge
ovs-vsctl add-br br0
# Create the tunnel to the other host and attach it to the
# br0 bridge
ovs-vsctl add-port br0 gre0 -- set interface gre0 type=gre options:remote_ip=$REMOTE_IP
# Add the br0 bridge to docker0 bridge
brctl addif $BRIDGE_NAME br0

# Some useful commands to confirm the settings:
# ip a s
# ip r s
# ovs-vsctl show
# brctl show
