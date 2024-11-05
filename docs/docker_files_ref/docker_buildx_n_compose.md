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
docker compose up/down to start/stopdo

# DOCKER COMPOSE ARCHIVE:
https://github.com/docker-archive/compose-cli/tree/main/docs

## TRYING THIS HASURA AND POSTGRES TUTORIAL
https://dev.to/raphaelmansuy/10-minutes-to-deploy-a-docker-compose-stack-on-aws-illustrated-with-hasura-and-postgres-3f6e
Feel like the stack is useful in any case - for condorGP not just tutorial
The docker compose learning is strong.

PROGRESS:
  AWS environment variables set on home machine
  AWS user group setup that has suitable permissions. Fairly coarse grain for now.
  Running .sh files works well.
  Cluster creation succeeded.

BUT
  CANNOT SSH INTO EC2 INSTANCE AND GET A REPLY...
Consider trying:
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html



# DIRECT TO AWS via DOCKER COMPOSE:
https://aws.amazon.com/blogs/containers/deploy-applications-on-amazon-ecs-using-docker-compose/
check out example yelb website:
https://github.com/mreferre/yelb/tree/master/deployments/platformdeployment

## Trying this:
https://dev.to/raphaelmansuy/10-minutes-to-deploy-a-docker-compose-stack-on-aws-illustrated-with-hasura-and-postgres-3f6e
### install ecs-cli:
https://github.com/aws/amazon-ecs-cli
Better:
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI.html
# ecs-cli command list:
https://docs.aws.amazon.com/cli/latest/reference/ecs/







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
