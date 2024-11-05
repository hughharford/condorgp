# Commands to ready images for docker compose

cd ~/code/hughharford/condorgp

## FIRST:

## ready condorgp:builder
docker build -t condorgp:builder -f docker_compose/docker_towards_compose/Dockerfile_builder .


## ready condorgp:check
docker build -t condorgp:check -f docker_compose/docker_towards_compose/Dockerfile_latest_wo_Naut_it .

## ready condorgp:cmd
docker build -t condorgp:cmd -f docker_compose/docker_towards_compose/Dockerfile_latest_wo_Naut_cmd .

## ready condorgp:worker
docker build -t condorgp:worker -f docker_compose/docker_towards_compose/Dockerfile_latest_wo_Naut_worker .

## THEN:

## run worker 1
docker run -it --name condorgp_1 condorgp:worker
## run worker 2
docker run -it --name condorgp_2 condorgp:worker

# run command
docker run -it --name condorgp_c condorgp:cmd
