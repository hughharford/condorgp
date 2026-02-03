#! \bin\bash

# docker run -it cg_nt_base:latest /bin/bash
DOCKER_IMAGE=cg_nt_base
DOCKER_TAG=latest

docker run \
--n=false \
-lxc-conf="lxc.network.type = veth" \
-lxc-conf="lxc.network.ipv4 = 172.17.0.1/16" \
-lxc-conf="lxc.network.ipv4.gateway = 172.17.0.2" \
-lxc-conf="lxc.network.link = docker0" \
-lxc-conf="lxc.network.name = ovs0" \
-lxc-conf="lxc.network.flags = up" \
-it $DOCKER_IMAGE:$DOCKER_TAG /bin/bash
