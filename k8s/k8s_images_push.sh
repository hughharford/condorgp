# copy images
export CGP_WORKER_IMAGE_NAME="cgp-nt-again"
microk8s ctr image import ../hughharford/00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME}.tar
