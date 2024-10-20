#! \bin\bash

# create network
docker network create cgp_net
# gives error but continues if extant

# inspect network
docker network inspect cgp_net

# connect rabbitmq
docker network connect cgp_net rabbitmq
# throws error if already connected

d
