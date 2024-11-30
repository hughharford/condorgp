#! \bin\bash

# remove to start fresh:

docker stop rabbitmq
docker stop cgp
docker stop cgp_worker

docker rm $(docker ps --filter status=exited -q)

docker network remove cgp_network

# start again

docker network create cgp_network

docker run -it -detached --rm --network cgp_network --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management


docker run -it -detached --network cgp_network --name cgp cgp_nt_base

docker run -it -detached --network cgp_network --name cgp_worker cgp_nt_base
