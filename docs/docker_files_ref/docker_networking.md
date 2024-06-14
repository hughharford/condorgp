
# https://www.baeldung.com/ops/docker-communicating-with-containers-on-same-machine

## to clear any previous networks
docker network prune

## run condorgp docker
docker run --rm -it --name condorgp condorgp:updates240611v6_bash 
docker run --rm -it --name condorgp2 condorgp:updates240611v6_bash 

## run rabbitmq docker
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

## check the docker dns status:
docker network inspect dns_default 
#### initially:
Error response from daemon: network dns_default not found

### https://docs.docker.com/network/drivers/bridge/

# but bridge network default is in place:
docker network inspect bridge  

# this includes the following: unnamed and now named condorgp container:
        "Containers": {
            "45871db5ee2a12ba485b6bd8314559aea9acf7c5eaf06902151c25bc8a61cf22": {
                "Name": "condorgp",
                "EndpointID": "d0d79ac17bde7d44a66552be6c71370c332d4515707b73fa0e414db7aed966a7",
                "MacAddress": "02:42:ac:11:00:04",
                "IPv4Address": "172.17.0.4/16",
                "IPv6Address": ""
            },
            "a45b27f22e62ae4b1bc1bdfeb6e63630efeff3b7fdd5f0ce55727505070b3e1c": {
                "Name": "rabbitmq",
                "EndpointID": "2398235853a145398bf43bac9e939a98db8aed3f510e91d4da8db4687de6152b",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "b72b2554f97e37408824401ee84770b078c29ad1eef104e34310658736801df6": {
                "Name": "friendly_fermat",
                "EndpointID": "70c015406988213b6df2f79b9133daf5ea2c3d6a7c90e648e3edaf431c62cd1b",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            }

# docker connections for rabbitmq:
https://github.com/deepshig/rabbitmq-docker

