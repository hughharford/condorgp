# copy images
export CGP_WORKER_IMAGE_NAME_1="cgp-nt-again"
export CGP_WORKER_IMAGE_NAME_2="cgpstar"
export CGP_WORKER_IMAGE_NAME_3="vsc-basic-python-7a94d97c7e4ae30dc4170673c9f8c8992e1b9f31abebe48ebc3675d5c971eeb6"

# ONE

# save file with:
docker save ${CGP_WORKER_IMAGE_NAME_1} > ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME_1}.tar

# import image with:
microk8s ctr image import ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME_1}.tar


# TWO

# save file with:
docker save ${CGP_WORKER_IMAGE_NAME_2} > ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME_2}.tar

# import image with:
microk8s ctr image import ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME_2}.tar


# THREE

# save file with:
docker save ${CGP_WORKER_IMAGE_NAME_3} > ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME_3}.tar

# import image with:
microk8s ctr image import ../00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME_3}.tar


#check images with
microk8s ctr images ls | grep cgp
