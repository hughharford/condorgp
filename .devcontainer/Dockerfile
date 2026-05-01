FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

ARG USERNAME=vscode

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      gnupg \
      lsb-release \
      make \
      jq && \
    rm -rf /var/lib/apt/lists/*

# kubectl
RUN curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg \
      https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key && \
    echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /" \
      > /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends kubectl && \
    rm -rf /var/lib/apt/lists/*

# docker CLI only (daemon remains on host via mounted socket)
RUN apt-get update && \
    apt-get install -y --no-install-recommends docker.io && \
    rm -rf /var/lib/apt/lists/*

# k3d
RUN curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Poetry pinned to project expectation
RUN python3 -m pip install --no-cache-dir poetry==1.8.4

USER ${USERNAME}
