# how to and record of work - Docker Buildx & Docker compose

## see Buildx below

# DOCKER COMPOSE
### REF: https://docs.docker.com/compose/gettingstarted/
This is obviously very powerful, and given that at least 4 containers will be
required, it'll be worth getting into.
These are:
-1 - rabbitmq (even if it's just one, when a cluster of 4 is recommended)
-2 - condorgp control
-3 - condorgp workers x2
-4 - condorgp db - fictional for now, but definitely will be required
-5 - condorgp checkpoints - also fictional for now, but functionality required

### **************** ****************** ****************** ******************
# TODO: come back to this later 
# Get started:
https://docs.docker.com/compose/gettingstarted/
This works nicely, once docker compose manually installed
# How compose works:
https://docs.docker.com/compose/compose-application-model/

### Manual installation:
https://docs.docker.com/compose/install/linux/#install-the-plugin-manually

## c.f. docker_compose in root folder

## Up / down
docker compose up/down to start/stop



# DIRECT TO AWS via DOCKER COMPOSE:
https://aws.amazon.com/blogs/containers/deploy-applications-on-amazon-ecs-using-docker-compose/
check out example yelb website:
https://github.com/mreferre/yelb/tree/master/deployments/platformdeployment

## Trying this:
https://dev.to/raphaelmansuy/10-minutes-to-deploy-a-docker-compose-stack-on-aws-illustrated-with-hasura-and-postgres-3f6e
### install ecs-cli:
https://github.com/aws/amazon-ecs-cli






# DOCKER BUILDX
This is the new way, so will be required.

### **************** ****************** ****************** ******************

# going to avoid Docker Desktop for Linux - low memory machine
https://docs.docker.com/desktop/install/linux-install/
Does look like it has some useful characteristics...

# manual install
https://github.com/docker/buildx#manual-download
This is unattended and will never get support, making it more likely to run 
the above and suffer the KVM overhead etc


# TODO: come back to this later 




