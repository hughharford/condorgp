#! \bin\bash

# setup builder and further multistage builds:
cd ~/code/hughharford/condorgp


# clear first
docker rm cgp_check condorgp_2 condorgp_1 condorgp_c

# BUILDS

## ready condorgp:builder
docker build -t condorgp:builder -f docker_compose/docker_files/Dockerfile_builder .


## ready condorgp:check
docker build -t condorgp:check -f docker_compose/docker_files/Dockerfile_latest_wo_Naut_check .

## ready condorgp:cmd
# docker build -t condorgp:cmd -f docker_compose/docker_files/Dockerfile_latest_wo_Naut_cmd .

## ready condorgp:worker
# docker build -t condorgp:worker -f docker_compose/docker_files/Dockerfile_latest_wo_Naut_worker .

## THEN:


# ## run worker 1
# docker run -it --name condorgp_1 condorgp:worker
# ## run worker 2
# docker run -it --name condorgp_2 condorgp:worker
# ## run command
# docker run -it --name condorgp_c condorgp:cmd

docker run -it --name cgp_check condorgp:check


# # create network
# docker network create cgp_net
# # gives error but continues if extant

# # inspect network
# docker network inspect cgp_net

# # connect rabbitmq
# docker network connect cgp_net rabbitmq
# # throws error if already connected
