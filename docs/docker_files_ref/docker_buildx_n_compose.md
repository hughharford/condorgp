# how to and record of work - Docker Buildx & Docker compose

# DOCKER COMPOSE
This is obviously very powerful, and given that at least 4 containers will be
required, it'll be worth getting into.
These are:
-1 - rabbitmq (even if it's just one, when a cluster of 4 is recommended)
-2 - condorgp control
-3 - condorgp workers x2
-4 - condorgp db - fictional for now, but definitely will be required
-5 - condorgp checkpoints - also fictional for now, but functionality required

### **************** ****************** ****************** ******************

# Get started:
https://docs.docker.com/compose/gettingstarted/

# TODO: come back to this later 


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




