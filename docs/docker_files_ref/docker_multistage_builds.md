
# standard task with pull specified
docker build --pull --rm -f "Dockerfile_latest" -t condorgp:latest "." 

# most basic, works but assumes Dockerfile is there, not named anything else
docker build -t condorgp:latest  . 

# -t for tag
# -f for file

# BUILDER
docker build -t condorgp:builder -f Dockerfile_builder . 

# WORKER
##      Build
docker build -t condorgp:latest_w -f Dockerfile_latest_worker . 
##      Run
docker run -it --name condorgp_1 condorgp:latest_w

# RUNNER
##      Build
docker build -t condorgp:latest_c -f Dockerfile_latest_cmd . 
##      Run
docker run -it --name condorgp_c condorgp:latest_c

# OVERALL
docker build -t condorgp:latest_it -f Dockerfile_latest_it . 
docker run -it --name condorgp_c_X condorgp:latest_it



# n___________________________-
# DELETE ALL STOPPED CONTAINERS:
docker rm $(docker ps --filter status=exited -q)
