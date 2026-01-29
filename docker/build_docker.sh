#!/bin/bash


DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile_new_start --target=cgp-nt-again -t cgp-nt-again .
