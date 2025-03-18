# copy images
export CGP_WORKER_IMAGE_NAME="cgp-nt-again"


#check images with
microk8s ctr images ls | grep cgp

# save file with:
docker save ${CGP_WORKER_IMAGE_NAME} > ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME}.tar

# import image with:
microk8s ctr image import ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME}.tar
