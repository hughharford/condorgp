#!/bin/bash

# copy images
export CGP_WORKER_IMAGE_NAME="cgp-nt-again"

export CGP_REGISTRY_NAME="cgp-registry" # note k3d adds "k3d-"

###### THIS WON'T WORK - HAVE TO RESET THE REGISTRY WHEN CLUSTER CREATED
# DELETE
#  microk8s ctr images rm docker.io/library/${CGP_WORKER_IMAGE_NAME}:latest


# delete image (by deleting registry)
# k3d registry delete k3d-cgp-registry.localhost
# k3d registry delete k3d-${CGP_REGISTRY_NAME}.localhost

# CREATE
# k3d registry create cgp-registry.localhost --port 30123


# save file with:
# docker save ${CGP_WORKER_IMAGE_NAME} > ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME}.tar


# IMPORT IMAGE TO REGISTRY

# import image with:
# microk8s ctr image import ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME}.tar

docker tag ${CGP_WORKER_IMAGE_NAME} ${CGP_REGISTRY_NAME}.localhost:30123/${CGP_WORKER_IMAGE_NAME}:latest
docker push ${CGP_REGISTRY_NAME}.localhost:30123/${CGP_WORKER_IMAGE_NAME}:latest
# i.e. image name for yamls:
# k3d-cgp-registry.localhost:30123/cgp-nt-again:latest

# CHECK
#check images with
# microk8s ctr images ls | grep cgp
curl http://localhost:30123/v2/_catalog # only for registry


# alternatively:
# k3d image import -c cgp-cluster cgp-nt-again -k
