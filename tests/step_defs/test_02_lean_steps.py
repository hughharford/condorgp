

import docker
from docker.utils import kwargs_from_env
import subprocess
import os
import sys


def run_bash():
    # subprocess.run(["bash","leanQC/run_docker.sh"]) # needs sudo
    os.system("sh leanQC/run_docker.sh") # doesn't need sudo


def check_docker_image(service: str, tag: str) -> bool:
    """Checks whether the given image for :service: with :tag: exists.

    :raises: ValueError if more than one docker image with :tag: found.
    :returns: True if there is exactly one matching image found.

    note: adapted from https://www.programcreek.com/python/?CodeExample=check+docker
    """
    docker_client = docker.from_env()
    docker_tag = service + ":" + tag
    images = docker_client.images.list()
    # image['RepoTags'] may be None
    # Fixed upstream but only in docker-py 2.
    # https://github.com/docker/docker-py/issues/1401
    print(images)
    result = [image for image in images if docker_tag in (image["RepoTags"] or [])]
    if len(result) > 1:
        raise ValueError(
            f"More than one docker image found with tag {docker_tag}\n{result}"
        )
    return len(result) == 1

if __name__ == "__main__":
    run_bash()
