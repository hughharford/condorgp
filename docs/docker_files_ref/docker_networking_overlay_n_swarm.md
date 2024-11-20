

### to show addresses:
ip addr show

interface enxf8e43b7937b7 has
192.168.1.167/24 brd 192.168.1.255:
    inet 192.168.1.167/24 brd 192.168.1.255 scope global dynamic noprefixroute enxf8e43b7937b7

### selecting
192.168.1.227 # not recognised as a system address

### trying
br-66a39f1f6abd

5: br-66a39f1f6abd: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:e1:81:46:dd brd ff:ff:ff:ff:ff:ff
    inet 172.19.0.1/16 brd 172.19.255.255 scope global br-66a39f1f6abd
       valid_lft forever preferred_lft forever

172.19.255.227

# DOCKER INSTRUCTIONS TO RUN OVERLAY WITH SWARM
### https://docs.docker.com/engine/network/tutorials/overlay/#use-an-overlay-network-for-standalone-containers

docker swarm init --advertise-addr
### but this needs an address specified
### docker specifically points to enxf8e43b7937b7
#### did not work: docker swarm init --advertise-addr 192.168.1.227


docker swarm init --advertise-addr 172.19.255.227
<!-- Error response from daemon: must specify a listening address because the address to advertise is not recognized as a system address, and a system's IP address to use could not be uniquely identified -->


## THIS WORKED to create docker swarm
### picked inet6 address
from the following:

7: enxf8e43b7937b7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether f8:e4:3b:79:37:b7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.167/24 brd 192.168.1.255 scope global dynamic noprefixroute enxf8e43b7937b7
       valid_lft 86396sec preferred_lft 86396sec
    inet6 2a02:6b6f:e6ba:f100:cf19:6d36:d780:bc40/64 scope global temporary dynamic
       valid_lft 604798sec preferred_lft 85952sec
    inet6 2a02:6b6f:e6ba:f100:64d5:d31f:7e88:6aad/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 628952sec preferred_lft 542552sec
    inet6 fe80::7ec7:b318:9815:c83d/64 scope link noprefixroute
       valid_lft forever preferred_lft forever

docker swarm init --advertise-addr 2a02:6b6f:e6ba:f100:cf19:6d36:d780:bc40

### got the following:
Swarm initialized: current node (zphubsw0txqvzh4g9o8tsgy6o) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-05hcib7uiear72cl41cpbp77n6r0m4rops32718a4jiizpgm1e-2pcl6a15226lk8bqf7vx12j5m [2a02:6b6f:e6ba:f100:cf19:6d36:d780:bc40]:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
