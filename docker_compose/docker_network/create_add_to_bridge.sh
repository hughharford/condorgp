

C1=aa
C2=bb

docker network remove cgp_net

docker network create cgp_net

docker network connect cgp_net $C1
docker network connect cgp_net $C2
