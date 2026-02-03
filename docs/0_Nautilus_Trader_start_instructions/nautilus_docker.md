# Instructions from the NT readme between the  # ***

# *********************************************************************

## Docker

Docker containers are built using a base `python:3.10-slim` with the following image variant tags:

- `nautilus_trader:latest` has the latest release version installed
- `nautilus_trader:develop` has the head of the `develop` branch installed
- `jupyterlab:develop` has the head of the `develop` branch installed along with `jupyterlab` and an
  example backtest notebook with accompanying data

The container images can be pulled as follows:

    docker pull ghcr.io/nautechsystems/<image_variant_tag> --platform linux/amd64

You can launch the backtest example container by running:

    docker pull ghcr.io/nautechsystems/jupyterlab:develop --platform linux/amd64
    docker run -p 8888:8888 ghcr.io/nautechsystems/jupyterlab:develop

Then open your browser at the following address:

    http://127.0.0.1:8888/lab


# *********************************************************************

# CondorGP attempts here:

## 1st, trying the below as indicated:
sudo docker pull ghcr.io/nautechsystems/nautilus_trader:latest --platform linux/amd64
### this worked, image loaded

## 2nd, run container
sudo docker run -it ghcr.io/nautechsystems/nautilus_trader:latest /bin/bash
### runs fine

## 3rd - be able to run a specific backtest in the container
A: first run an example outside the container
B: enable shared folder into container to allow new scripts and log files
