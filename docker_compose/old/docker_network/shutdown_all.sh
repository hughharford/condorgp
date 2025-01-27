docker stop rabbitmq
docker stop cgp
docker stop cgp_worker

docker rm $(docker ps --filter status=exited -q)  

docker network remove cgp_network 
